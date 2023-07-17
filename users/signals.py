from django.db.models.signals import(
    post_save,
    pre_save,
    post_delete
)
import os
from django.dispatch import receiver
from .models import UserProfile, User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import Article


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Создает или обновляет профиль пользователя при сохранении модели User.

    Параметры:
        - sender(User): Класс-отправитель сигнала.
        - instance(User): Объект пользователя.
        - created (bool): Флаг, указывающий, был ли создан объект пользователем.
        - **kwargs: Дополнительные именованные аргументы.
    """
    if created:
        if instance.is_staff:
            content_type = ContentType.objects.get_for_model(Article)
            article_permissions = Permission.objects.filter(
                content_type=content_type)
            for perm in article_permissions:
                instance.user_permissions.add(perm)
        UserProfile.objects.create(user=instance)
        instance.user_profile.save()
    else:
        pass


@receiver(pre_save, sender=UserProfile)
def delete_previous_image(sender, instance, **kwargs):
    """
    Сигнал, выполняющийся перед сохранением экземпляра UserProfile.
    Удаляет предыдущее изображение, связанное с экземпляром UserProfile, если оно было изменено.

    Аргументы:
        sender (UserProfile): Отправитель сигнала - модель UserProfile
        instance (UserProfile): Сохраняемый экземпляр UserProfile.
        **kwargs: Дополнительные именованные аргументы.

    Возвращаемое значение:
        None
    """
    if instance.pk:
        try:
            previous_user_profile = UserProfile.objects.get(pk=instance.pk)
            if previous_user_profile.avatar != instance.avatar:
                if previous_user_profile.avatar:
                    if os.path.isfile(previous_user_profile.avatar.path):
                        os.remove(previous_user_profile.avatar.path)

        except UserProfile.DoesNotExist:
            pass

@receiver(post_delete, sender=UserProfile)
def delete_previous_image(sender, instance, **kwargs):
    """
    Сигнал, выполняемая после удаления экземпляра UserProfile.
    Удаляет предыдущее изображение, связанное с экземпляром UserProfile, если изображение существует

    Аргументы:
        sender (UserProfile): Отправитель сигнала.
        instance (UserProfile): Удаленный экземпляр UserProfile.
        **kwargs: Дополнительные именованные аргументы.

    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

#ed791554893287ee7ee116c467d8972b73118bca
#c398462df0ddd6e95c00c96a412ced3872030b9e -session