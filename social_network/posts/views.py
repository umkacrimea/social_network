# posts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from .models import Post, PostImage, Comment, Like
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    CommentListSerializer, CommentDetailSerializer
)


# =============================================================================
# 🔐 Permissions
# =============================================================================
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Разрешить чтение всем, запись только авторизованным"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Только автор может редактировать/удалять"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """Только автор комментария может редактировать/удалять"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# =============================================================================
# 📝 POST VIEWS
# =============================================================================
class PostListCreateView(generics.ListCreateAPIView):
    """Список постов + создание нового"""
    queryset = Post.objects.prefetch_related('images', 'likes').select_related('author')
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        return PostListSerializer
    
    def get_queryset(self):
        return Post.objects.prefetch_related('images', 'likes', 'comments').select_related('author')
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        images = self.request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали поста + редактирование + удаление"""
    permission_classes = [IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_serializer_class(self):
        return PostDetailSerializer
    
    def get_queryset(self):
        return Post.objects.prefetch_related('images', 'likes', 'comments').select_related('author')
    
    def update(self, request, *args, **kwargs):
        """Обновление поста с поддержкой новых изображений"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        
        # Обработка новых изображений
        images = request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)
        
        return Response(PostDetailSerializer(post, context={'request': request}).data)


# =============================================================================
# 💬 COMMENT VIEWS (консолидированные)
# =============================================================================
class CommentListView(generics.ListCreateAPIView):
    """Список комментариев поста + создание нового"""
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id).select_related('author').order_by('-created_at')
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Детали комментария + редактирование + удаление (ОДИН эндпоинт)"""
    queryset = Comment.objects.select_related('author', 'post')
    permission_classes = [IsCommentAuthorOrReadOnly]
    
    def get_serializer_class(self):
        return CommentDetailSerializer


# =============================================================================
# ❤️ LIKE VIEWS
# =============================================================================
class LikeToggleView(APIView):
    """Лайк/анлайк поста"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        """Поставить лайк"""
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        return Response({
            'liked': True,
            'likes_count': post.likes.count(),
            'message': 'Лайк поставлен' if created else 'Уже лайкнуто'
        })
    
    def delete(self, request, post_id):
        """Убрать лайк"""
        post = get_object_or_404(Post, pk=post_id)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        
        return Response({
            'liked': False,
            'likes_count': post.likes.count(),
            'message': 'Лайк удалён' if deleted else 'Лайка не было'
        })


class PostLikeStatusView(APIView):
    """Проверить статус лайка для текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
        
        return Response({
            'post_id': post_id,
            'is_liked': is_liked,
            'likes_count': post.likes.count()
        })