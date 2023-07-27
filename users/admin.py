from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _


class UserProfileInline(admin.StackedInline):
    """
    Класс Inline для профиля пользователя в административном интерфейсе.
    Атрибуты:
        - model (Model): Модель для Inline.
        - can_delete (bool): Указывает, можно ли удалить профиль.
        - verbose_plural_name (str): Полное именование во множественном числе для профиля.
        - fk_name (str): Название внешнего ключа для отношения.
    """
    model = UserProfile
    can_delete = False
    verbose_plural_name = _('Profile of User')
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    """
    Класс администратора для пользовательской модели.

    Атрибуты:
        - add_form (Form): Форма для добавления нового пользователя.
        - form (Form): Форма для редактирования существующего пользователя.
        - model (Model): Модель для класса администратора.
        - list_display_links (list): Поля, которые должны быть связаны со страницей изменений для пользователя.
        - search_fields (tuple): Поля, по которым можно осуществлять поиск в административном интерфейсе.
        - ordering (tuple): Поля, которые должны использоваться для упорядочивания пользователей.
        - inlines (tuple): Классы Inline, включаемые в административный интерфейс.
        - list_display (tuple): Поля, которые отображаются в представлении списка пользователей.
        - list_filter (tuple): Поля, которые используются для фильтрации пользователей.
        - fieldsets (tuple): Наборы полей, используемые для редактирования данных пользователя.
        - add_fieldsets (tuple): Наборы полей, используемые для добавления нового пользователя.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = ["email"]
    search_fields = ("email",)
    ordering = ("email",)
    inlines = (UserProfileInline,)
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_moderator",
        "is_superuser",
    )
    list_filter = ("email", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal Information"),
            {"fields": ("email",)},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_moderator",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Imortant"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    'is_moderator',
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        '''Возвращает список встроенных параметров администрирования для связанных моделей.

        Если `obj` не указан, вернуть пустой список. В противном случае вызвать родительский
        метод `get_inline_instances` класса, передавая `request` и `obj`
        аргументы.

        Аргументы:
        self: экземпляр CustomUserAdmin.
        запрос: экземпляр HttpRequest передается в представление администратора.
        obj: редактируемый экземпляр модели или None.

        Возвращает:
        Список экземпляров InlineModelAdmin или пустой список.
        '''

        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
