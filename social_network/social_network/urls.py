from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),

    # Frontend страницы
    path('', views.posts_view, name='home'),
    path('login/', views.login_view, name='login-page'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('posts/', views.posts_view, name='posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)