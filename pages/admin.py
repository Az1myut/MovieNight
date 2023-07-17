from django.contrib import admin
from .models import (
    FooterSocial,
    FooterUsefulLink,
    NaviItem
)
# Register your models here.


@admin.register(FooterUsefulLink)
class FooterUsefulLinkModelAdmin(admin.ModelAdmin):
    """
    Админка для управления объектами FooterUsefulLink

    Атрибуты:
    list_display(list) - поля объекта FooterUsefulLink для отображения
    list_display_links(list) - поля объекта FooterUsefulLink для ссылки

    """
    list_display = ['pk', 'title',]
    list_display_links = ['title',]


@admin.register(FooterSocial)
class FooterSocialModelAdmin(admin.ModelAdmin):
    """
    Админка для управления объектами FooterSocial

    Атрибуты:
    list_display(list) - поля объекта FooterSocial для отображения
    list_display_links(list) - поля объекта FooterSocial для ссылки

    """
    list_display = ['pk', 'title',]
    list_display_links = ['title',]


@admin.register(NaviItem)
class NaviItemModelAdmin(admin.ModelAdmin):
    """
    Админка для управления объектами NaviItem

    Атрибуты:
    list_display(list) - поля объекта NaviItem для отображения
    list_display_links(list) - поля объекта NaviItem для ссылки

    """
    list_display = ['pk', 'title',]
    list_display_links = ['title',]
