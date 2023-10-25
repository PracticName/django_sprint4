from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DeleteView, DetailView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from . forms import PostForm, CustomUserCreationForm

from .models import Category, Post, User


'''class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:profile')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')'''


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


@login_required
def create_post(request, post_id=None):
    template = 'blog/create.html'
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)
    else:
        instance = None
    form = PostForm(request.POST or None, files=request.FILES or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)


def index(request):
    template = 'blog/index.html'
    posts = create_post_request()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        create_post_request(),
        pk=id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    posts = create_post_request().filter(category=category)
    paginator = Paginator(posts, 10)
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
