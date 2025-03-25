from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для постов (создание, чтение, обновление, удаление)."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        user = self.request.user
        if serializer.instance.author != user:
            raise PermissionDenied("Нельзя редактировать чужой пост")
        serializer.save()

    def perform_destroy(self, post):
        user = self.request.user
        if post.author != user:
            raise PermissionDenied("Нельзя удалить чужой пост")
        post.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для информации о группах (только для чтения)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=author, post=post)

    def perform_update(self, serializer):
        user = self.request.user
        if serializer.instance.author != user:
            raise PermissionDenied("Нельзя редактировать чужой комментарий")
        serializer.save()

    def perform_destroy(self, comment):
        user = self.request.user
        if comment.author != user:
            raise PermissionDenied("Нельзя удалить чужой комментарий")
        comment.delete()
