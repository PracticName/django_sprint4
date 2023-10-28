from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
#  from django.contrib.auth.forms import UserCreationForm
from . forms import PostForm, CustomUserCreationForm, CommentForm

from .models import Category, Post, User, Comment


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


'''@login_required
def create_post(request, post_id=None):
    template = 'blog/create.html'
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id, author=request.user)
    else:
        instance = None
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance)
    context = {'form': form}
    if form.is_valid():
        form_obj = form.save(commit=False)
        form_obj.author = request.user
        form.save()
        return redirect('blog:profile')
    return render(request, template, context)'''


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
        get_object_or_404(Post, pk=kwargs['post_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['post_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.object.author})


class PostListView(ListView):
    model = Post
    paginate_by = settings.POSTS_NUMBER
    template_name = 'blog/index.html'
    queryset = create_post_request()
    context_object_name = 'post'

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_count'] = Comment.objects.count()
        return context'''


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    def get_success_url(self) -> str:
        post_id = self.kwargs['post_id']
        return reverse('blog:post_detail', kwargs={'post_id': post_id})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comment, pk=kwargs['comment_id'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    context_object_name = 'comment'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comment, pk=kwargs['comment_id'], author=request.user)
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
    posts = create_post_request().filter(category=category)
    paginator = Paginator(posts, settings.POSTS_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'post_list': posts, 'page_obj': page_obj}
    return render(request, template, context)


# Страница пользователя
def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    posts = create_post_request().filter(author=profile.pk)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}

    return render(request, template, context)


@login_required
def edit_profile(request, username):
    template = 'blog/user.html'
    instance = get_object_or_404(User, username=username)
    form = CustomUserCreationForm(request.POST, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


'''@login_required
def add_comment(request, post_id, comment_id=None):
    instance = get_object_or_404(
        create_post_request(),
        pk=post_id
    )
    form = CommentForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.post = instance
        comments.save()
    return redirect('blog:post_detail', post_id)'''


'''@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile')
    return render(request, 'blog/create.html', context)'''


'''@login_required
def delete_comment(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile')
    return render(request, 'blog/comment.html', context)'''
