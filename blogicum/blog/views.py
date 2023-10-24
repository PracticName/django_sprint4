from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DeleteView, DetailView, ListView
from django.utils.timezone import now

from .models import Category, Post, User


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


def index(request):
    template = 'blog/index.html'
    posts = create_post_request()[:settings.POST_QUANTITY]
    context = {'post_list': posts}
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
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)


# Страница пользователя
def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    context = {'profile': profile}

    return render(request, template, context)
