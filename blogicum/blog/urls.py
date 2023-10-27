from django.urls import path

from blog import views
from . views import PostDetailView, PostDeleteView, PostCreateView, PostUpdateView, PostListView, CommentUpdateView, CommentDeleteView, CommentCreateView


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
        'profile/<slug:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'profile/<slug:username>/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path('', PostListView.as_view(), name='index'),
]
