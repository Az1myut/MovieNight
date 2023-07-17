from django.contrib import admin
from .models import Actor
# Register your models here.

@admin.register(Actor)
class AdminActor(admin.ModelAdmin):
    """
    Админка для управления объектами Actor

    Атрибуты:
    list_display(list) - поля объекта Actor для отображения
    search_fields(list) - поля объекта Actor для поиска
    list_display_links(list) - поля объекта Actor для ссылки
    list_filter(list) - поля объекта Actor для фильтрации
    
    """
    search_fields = ('name',)
    list_display = ['pk','name', 'birth_date']
    list_display_links = ('name',)
    list_filter = ( 'name','popularity')