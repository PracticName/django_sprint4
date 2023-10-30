from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, EditRegistrationForm, PostForm
from .models import Category, Comment, Post, User


def create_post_request():
    return Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        pub_date__lt=now(),
        is_published=True,
        category__is_published=True
    )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:   
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Post, pk=kwargs['post_id'], author=self.request.user.pk
        )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.object.author})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class PostListView(ListView):
    model = Post
    paginate_by = settings.POSTS_NUMBER
    template_name = 'blog/index.html'
    queryset = create_post_request()
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = get_object_or_404(User, username=self.object.author)
        if self.request.user != user_name:
            post = get_object_or_404(
                Post,
                pk=self.kwargs['post_id'],
                pub_date__lt=now(),
                is_published=True,
                category__is_published=True
            )
        else:
            post = get_object_or_404(
                Post,
                pk=self.kwargs['post_id']
            )
        context['post'] = post
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('blog:post_detail', kwargs={'post_id': post_id})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Comment, pk=kwargs['comment_id'], author=request.user.pk
        )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('blog:post_detail', kwargs={'post_id': post_id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Comment, pk=kwargs['comment_id'], author=request.user.pk
        )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('blog:post_detail', kwargs={'post_id': post_id})


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    posts = create_post_request().filter(category=category).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
    paginator = Paginator(posts, settings.POSTS_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'post_list': posts, 'page_obj': page_obj}
    return render(request, template, context)


class ProfileDetailView(DetailView):
    model = User
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'blog/profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user != self.object:
            posts = create_post_request().filter(author=self.object)
        else:
            posts = Post.objects.select_related(
                'location',
                'author',
                'category').filter(author=self.object)
        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

        paginator = Paginator(posts, settings.POSTS_NUMBER)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditRegistrationForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        username = self.object.username
        return reverse('blog:profile', kwargs={'username': username})
