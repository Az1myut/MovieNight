from django.contrib import admin
from .models import (
    Movie, Genre, Keyword
)
# Register your models here.


def make_released(modeladmin, request, queryset):
    """
    Помечает объекты модели как "выпущенные".

    Параметры:
        - modeladmin: Административная модель.
        - request: Запрос пользователя.
        - queryset: Выборка объектов.
    """
    queryset.update(is_released=True)


make_released.short_description = "Released"


def make_unreleased(modeladmin, request, queryset):
    """
    Помечает объекты модели как "не выпущенные".

    Параметры:
        - modeladmin: Административная модель.
        - request: Запрос пользователя.
        - queryset: Выборка объектов.
    """
    queryset.update(is_released=False)


make_unreleased.short_description = "Not Released"


@admin.register(Movie)
class AdminMovie(admin.ModelAdmin):
    """
    Админка для управления объектами Movie

    Атрибуты:
    list_display(list) - поля объекта Actor для отображения
    search_fields(list) - поля объекта Actor для поиска
    list_display_links(list) - поля объекта Actor для ссылки
    list_filter(list) - поля объекта Actor для фильтрации
    actions(list) - поля объекта Actor для действий
    list_editable(list) - поля объекта Actor для изменения

    """
    actions = [make_released, make_unreleased]
    search_fields = ('title',)
    list_editable = ['is_released',]
    list_display = ['pk', 'title', 'is_released', 'original_language']
    list_display_links = ('title',)
    list_filter = ('title', 'popularity', 'vote_average', 'original_language')

    def get_list_display_links(self, request, list_display):
        """
        Возвращает ссылки для отображения объектов модели на странице списка.

        Параметры:
            - request: Запрос пользователя.
            - list_display: Список полей для отображения.

        Возвращает:
            - list_display_links (list): Список полей для отображения в виде ссылок.
            - None: Если пользователь не является суперпользователем.
        """
        if (not request.user.is_superuser):
            return None
        else:
            return ['title']

    def get_list_filter(self, request):
        """
        Возвращает список полей для фильтрации на странице списка.

        Параметры:
            - request: Запрос пользователя.

        Возвращает:
            - f_d (list): Список полей для фильтрации.
        """
        f_d = ['is_released']
        if (request.user.is_superuser):
            f_d += ['title', 'popularity', 'vote_average', 'original_language']
        return f_d


admin.site.register(Genre)
admin.site.register(Keyword)
