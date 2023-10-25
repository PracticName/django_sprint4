from django.urls import path

from blog import views


app_name = 'blog'

urlpatterns = [
    path(
        'posts/<int:id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.create_post,
        name='edit_post'
    ),
    path(
        'posts/create/',
        views.create_post,
        name='create_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path('', views.index, name='index'),
]
