from django.contrib import admin
from .models import ContactPage, ContactMessage
# Register your models here.
admin.site.register(ContactPage)


@admin.register(ContactMessage)
class AdminContanctMessage(admin.ModelAdmin):
    """
    Админка для модели ContactMessage.

    Этот класс определяет настройки административной панели для модели ContactMessage.
    Регистрирует модель ContactMessage с административной панелью.

    Атрибуты:
        search_fields (tuple): Поля, по которым будет выполняться поиск.
        list_display (list): Поля, отображаемые в списке объектов.
        list_display_links (tuple): Поля, являющиеся ссылками на объекты в списке.
        list_filter (tuple): Поля, по которым можно фильтровать список объектов.

    """
    search_fields = ('subject',)
    list_display = ['subject', 'email']
    list_display_links = ('subject',)
    list_filter = ('name', 'email')
