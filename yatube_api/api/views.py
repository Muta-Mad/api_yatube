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
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Нельзя редактировать чужой пост")
        super().perform_update(serializer)

    def perform_destroy(self, post):
        if post.author != self.request.user:
            raise PermissionDenied("Нельзя удалить чужой пост")
        super().perform_destroy(post)


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
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs['post_id'])
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Нельзя редактировать чужой комментарий")
        super().perform_update(serializer)

    def perform_destroy(self, comment):
        if comment.author != self.request.user:
            raise PermissionDenied("Нельзя удалить чужой комментарий")
        super().perform_destroy(comment)
