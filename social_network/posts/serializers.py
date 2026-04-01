from rest_framework import serializers
from .models import Post, PostImage, Comment, Like
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = fields


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


# =============================================================================
# 📋 Comment Serializers
# =============================================================================
class CommentListSerializer(serializers.ModelSerializer):
    """Лёгкий сериализатор для списка комментариев"""
    author = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class CommentDetailSerializer(serializers.ModelSerializer):
    """Полный сериализатор для деталей комментария"""
    author = UserMinimalSerializer(read_only=True)
    is_author = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'is_author']
        read_only_fields = ['id', 'author', 'created_at']
    
    def get_is_author(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.author
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


# =============================================================================
# 📝 Post Serializers
# =============================================================================
class PostListSerializer(serializers.ModelSerializer):
    """Лёгкий сериализатор для списка постов (без комментариев)"""
    author = UserMinimalSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentListSerializer(many=True, read_only=True) 
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'images', 'comments',  
                  'likes_count', 'is_liked', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    """Полный сериализатор для деталей поста (с комментариями)"""
    author = UserMinimalSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'images', 'comments', 'likes_count', 
                  'is_liked', 'comments_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)