# posts/urls.py
from django.urls import path
from .views import (
    PostListCreateView, PostDetailView,
    CommentListView, CommentDetailView,
    LikeToggleView, PostLikeStatusView
)

urlpatterns = [
    # ========================================================================
    # POSTS
    # ========================================================================
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # ========================================================================
    # COMMENTS (консолидированная структура)
    # ========================================================================
    # Список комментариев поста + создание
    path('<int:post_id>/comments/', CommentListView.as_view(), name='comment-list'),
    
    # Детали комментария + редактирование + удаление (ОДИН эндпоинт)
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    
    # ========================================================================
    # LIKES
    # ========================================================================
    path('<int:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('<int:post_id>/like-status/', PostLikeStatusView.as_view(), name='like-status'),
]