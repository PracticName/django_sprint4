from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Category, Post


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
