from blog import views

from django.urls import path

from .views import (CommentCreateView, CommentDeleteView, CommentUpdateView,
                    PostCreateView, PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView, ProfileDetailView,
                    ProfileUpdateView)

app_name = 'blog'

urlpatterns = [
    path(
        'posts/<int:post_id>/',
        PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    #  страница полььзователя
    path(
        'profile/edit/',
        ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<slug:username>/',
        ProfileDetailView.as_view(),
        name='profile'
    ),
    path('', PostListView.as_view(), name='index'),
]
