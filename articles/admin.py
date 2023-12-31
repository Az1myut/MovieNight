from django.contrib import admin
from .models import (
    Article,
    Comment,
)
from icecream import ic
# Register your models here.

def make_approved(modeladmin, request, queryset):
    """
    Помечает объекты модели как "выпущенные".

    Параметры:
        - modeladmin: Административная модель.
        - request: Запрос пользователя.
        - queryset: Выборка объектов.
    """
    queryset.update(approved=True)


make_approved.short_description = "Approved"


def make_unapproved(modeladmin, request, queryset):
    """
    Помечает объекты модели как "не выпущенные".

    Параметры:
        - modeladmin: Административная модель.
        - request: Запрос пользователя.
        - queryset: Выборка объектов.
    """
    queryset.update(approved=False)


make_unapproved.short_description = "Not Approved"

@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    """
    Админка для управления объектами модели Article.

    Атрибуты:
        search_fields (tuple): Поля, используемые для поиска статей.
        list_display (list): Поля, отображаемые в списке статей.
        list_display_links (tuple): Поля, которые являются ссылками на детальное представление статей.
        list_filter (tuple): Поля, используемые для фильтрации статей.

    """
    actions = [make_approved, make_unapproved]
    search_fields = ('title',)
    list_display = ['pk', 'title', 'author', 'approved']
    list_display_links = ('title',)
    list_filter = ('updated_at',)


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    """
    Админка для управления объектами для модели Comment.

    Атрибуты:
        search_fields (tuple): Поля, используемые для поиска комментариев.
        list_display (list): Поля, отображаемые в списке комментариев.
        list_display_links (tuple): Поля, которые являются ссылками на детальное представление комментариев.
        list_filter (tuple): Поля, используемые для фильтрации комментариев.

    Методы:
        get_text(obj): Возвращает сокращенную версию текста комментария.
    """
    search_fields = ('text',)
    list_display = ['pk', 'author', 'get_text']
    list_display_links = ('pk',)
    list_filter = ('updated_at',)

    def get_text(self, obj):
        """
        Возвращает сокращенную версию текста комментария.

        Аргументы:
            obj (Comment): Объект комментария .

        Возвращает:
            str: Сокращенный текст комментария.
        """
        return obj.text[:40]
