# posts/signals.py
import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import PostImage

@receiver(pre_delete, sender=PostImage)
def delete_image_file(sender, instance, **kwargs):
    """Удаляет файл изображения при удалении модели PostImage"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"🗑️ Удалён файл: {instance.image.path}")
        except Exception as e:
            print(f"❌ Ошибка при удалении файла: {e}")

@receiver(pre_save, sender=PostImage)
def delete_old_image_file(sender, instance, **kwargs):
    """Удаляет старый файл изображения при замене на новое"""
    if not instance.pk:
        return  # Новый объект, ничего не удаляем
    
    try:
        old_instance = PostImage.objects.get(pk=instance.pk)
    except PostImage.DoesNotExist:
        return
    
    old_image = old_instance.image
    new_image = instance.image
    
    # Если файл изменился и старый существует — удаляем
    if old_image and new_image and old_image != new_image and os.path.isfile(old_image.path):
        try:
            os.remove(old_image.path)
            print(f"🗑️ Заменён файл: {old_image.path}")
        except Exception as e:
            print(f"❌ Ошибка при замене файла: {e}")