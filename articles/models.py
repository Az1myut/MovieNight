from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete, pre_init
from guardian.shortcuts import assign_perm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from icecream import ic
import os
import uuid


@receiver(pre_save, sender='articles.Article')
def delete_previous_image(sender, instance, **kwargs):
    """
    Сигнал, выполняющийся перед сохранением экземпляра Article.
    Удаляет предыдущее изображение, связанное с экземпляром Article, если оно было изменено.

    Аргументы:
        sender (Article): Отправитель сигнала - модель Article
        instance (Article): Сохраняемый экземпляр Article.
        **kwargs: Дополнительные именованные аргументы.

    Возвращаемое значение:
        None
    """
    if instance.pk:
        try:
            previous_article = Article.objects.get(pk=instance.pk)
            if previous_article.image != instance.image:
                if previous_article.image:
                    if os.path.isfile(previous_article.image.path):
                        os.remove(previous_article.image.path)

        except Article.DoesNotExist:
            pass


class Article(models.Model):
    """
    Модель, представляющая статью.

    Атрибуты:
        author (ForeignKey): Автор статьи.
        title (str): Заголовок статьи.
        slug (slug): Слаг  статьи.
        content (str): Содержание статьи.
        image (file): Изображение, связанное со статьей.
        created_at (datetime): Метка времени создания статьи.
        updated_at (datetime): Метка времени последнего обновления статьи.
        approved (bool): Индикатор одобрения статьи.

    Методы:
        __str__(): Возвращает строковое представление статьи.
        save(): Сохраняет статью и генерирует слаг на основе заголовка.
        get_absolute_url(): Возвращает абсолютный URL статьи.
        get_number_comments(): Возвращает количество комментариев к статье.
    """
    author = models.ForeignKey(
        verbose_name="Author", to=User, on_delete=models.CASCADE,
        related_name='author_articles'
    )
    title = models.CharField(verbose_name="Ttile", max_length=256, unique=True)
    slug = models.SlugField(verbose_name="slug", blank=True, unique=True)
    content = models.TextField(verbose_name="Content")
    image = models.ImageField(verbose_name="Image",
                              upload_to="articles/", blank=True, null=True)
    created_at = models.DateTimeField(
        verbose_name="Created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated", auto_now=True)
    approved = models.BooleanField(verbose_name='Aproved', default=False)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['updated_at',]

    def __str__(self) -> str:
        """
        Возвращает строковое представление статьи в виде его заголовка
        """
        return f"{self.title}"

    def save(self, *args, **kwargs):
        """
        Генерирует слаг на основе заголовка  и сохраняет статью

        Аргументы:
            *args: Дополнительные  аргументы.
            **kwargs: Дополнительные именованные аргументы.


        """
        self.slug = slugify(_(self.title))
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Возвращает:
            str: Абсолютный URL статьи.
        """
        from django.urls import reverse
        return reverse("articles:article_detail", kwargs={"slug": self.slug})

    def get_number_comments(self):
        """
        Возвращает:
            int: Количество комментариев к статье.
        """
        article_comments = self.article_comments
        if article_comments:
            return len(article_comments.all())
        return 0


@receiver(post_save, sender=Article)
def create_or_update_artcile(sender, instance, created, **kwargs):
    """
    Сигнал, выполняющийся после сохранения экземпляра Article.
    Назначает права доступа автору статьи на основе экземпляра статьи

    Аргументы:
        sender (Article): Отправитель сигнала.
        instance (Article): Сохраненный экземпляр Article.
        created (bool): Индикатор, указывающий, был ли создан новый экземпляр.
        **kwargs: Дополнительные именованные аргументы.

    """
    if created:
        content_type = ContentType.objects.get_for_model(Article)
        article_permissions = Permission.objects.filter(content_type=content_type)
        author = instance.author

        for perm in article_permissions:
            assign_perm(perm=f'articles.{perm.codename}',
                        obj=instance, user_or_group=author)


@receiver(post_delete, sender=Article)
def delete_previous_image(sender, instance, **kwargs):
    """
    Сигнал, выполняемая после удаления экземпляра Article.
    Удаляет предыдущее изображение, связанное с экземпляром Article, если изображение существует

    Аргументы:
        sender (Article): Отправитель сигнала.
        instance (Article): Удаленный экземпляр Article.
        **kwargs: Дополнительные именованные аргументы.

    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender='articles.Comment')
def set_unique_uuid(sender, instance, **kwargs):
    """
    Сигнал, выполняемый перед сохранением экземпляра Comment.
    Устанавливает уникальный идентификатор UUID для экземпляра Comment, если он не установлен.

    Аргументы:
        sender (Comment): Отправитель сигнала.- модель Comment
        instance (Comment): Сохраняемый экземпляр Comment.
        **kwargs: Дополнительные именованные аргументы.

    """
    if instance.uuid:
        pass
    else:
        uuid_id = uuid.uuid4()
        while Comment.objects.filter(uuid=uuid_id):
            uuid_id = uuid.uuid4()
        instance.uuid = uuid_id


class Comment(models.Model):
    """
    Модель, представляющая комментарий к статье.

    Атрибуты:
        article (ForeignKey): Статья, к которой относится комментарий.
        author (ForeignKey): Автор комментария.
        uuid (uuid): Уникальный идентификатор UUID комментария.
        text (str): Текст комментария.
        created_at (datetime): Метка времени создания комментария.
        updated_at (datetime): Метка времени последнего обновления комментария.

    Методы:
        __str__(): Возвращает строковое представление комментария.
    """
    article = models.ForeignKey(
        verbose_name="Article", to=Article, on_delete=models.CASCADE,
        related_name='article_comments'
    )
    author = models.ForeignKey(
        verbose_name="Author",
        to=User,
        on_delete=models.CASCADE,
        related_name='author_comments'
    )
    parent_comment = models.ForeignKey(verbose_name='Parent Comment',to='self',on_delete=models.CASCADE,
                                        blank=True, null=True, related_name= 'child_comments' )

    uuid = models.UUIDField(null=True, blank=True, editable=False, unique=True)
    text = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(
        verbose_name="Created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated", auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['article',]

    def __str__(self) -> str:
        """
        Возвращает строковое представление комментария в виде юзернейма автора
        и послдених 30 символов в тексте коментария если есть юзернейм
        Если нет, то вместо юзернейма возвращается Unknown

        Возвращает:
            str: Строковое представление комментария.
        """

        return f"{self.author} - {self.text[:30]}"
    def get_comments_recursively(self, comment, all_comments):
        
        if len(comment.child_comments.all()) > 0:
            for child_comment in comment.child_comments.all():
                all_comments.append(child_comment)
                all_comments = self.get_comments_recursively(comment=child_comment, all_comments=all_comments)
            return all_comments
        else:
            return all_comments 
    def get_all_child_comments(self):
        child_comments = self.get_comments_recursively(comment=self,all_comments=[])
        ic(child_comments)
        return child_comments
