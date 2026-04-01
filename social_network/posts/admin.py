from django.contrib import admin
from django.utils.html import format_html
from .models import Post, PostImage, Comment, Like  

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'text_preview', 'created_at', 'likes_count', 'comments_count']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def text_preview(self, obj):
        return (obj.text[:50] + '…') if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = '❤️ Лайки'
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = '💬 Комментарии'


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'image_preview', 'uploaded_at']
    list_filter = ['uploaded_at']
    readonly_fields = ['uploaded_at', 'image_tag']
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border-radius: 4px;">',
                obj.image.url
            )
        return '—'
    image_preview.short_description = 'Превью'
    
    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; border-radius: 8px;">',
                obj.image.url
            )
        return '—'
    image_tag.short_description = 'Изображение'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post_link', 'text_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'post__text']
    readonly_fields = ['created_at']
    
    def post_link(self, obj):
        return format_html(
            '<a href="/admin/posts/post/{}/change/" target="_blank">Post #{}</a>',
            obj.post.id,
            obj.post.id
        )
    post_link.short_description = 'Пост'
    
    def text_preview(self, obj):
        return (obj.text[:50] + '…') if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Комментарий'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post_link', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__text']
    readonly_fields = ['created_at']
    
    def post_link(self, obj):
        return format_html(
            '<a href="/admin/posts/post/{}/change/" target="_blank">Post #{}</a>',
            obj.post.id,
            obj.post.id
        )
    post_link.short_description = 'Пост'