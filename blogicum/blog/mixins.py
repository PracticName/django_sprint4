from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Comment, Post


class PostMixin:
    model = Post
    template_name = 'blog/create.html'


class PostDispatchmixin:
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    context_object_name = 'comment'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('blog:post_detail', kwargs={'post_id': post_id})


class CommentDispathMixin:
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Comment, pk=kwargs['comment_id'], author=request.user.pk
        )
        return super().dispatch(request, *args, **kwargs)
