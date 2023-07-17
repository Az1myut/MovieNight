from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .validators import validate_age, validate_phone_number
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from movies.models import Movie
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель представления пользователя

    Атрибуты:
    - email (email): Адрес электронной почты пользователя.
    - is_staff (bool): Указывает, имеет ли пользователь привилегии персонала.
    - is_superuser (bool): Указывает, имеет ли пользователь привилегии суперпользователя.
    - is_active (boll): Указывает, активен ли пользовательский аккаунт.
    - last_login (date): Дата и время последнего входа пользователя.
    - date_joined (date): Дата и время присоединения пользователя.
    """
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserProfile(models.Model):
    """
    Модель представления профиля пользователся
    Атрибуты:
        - user (OneToOneField): Пользователь, связанный с профилем.
        - birth_date (date): Дата рождения пользователя.
        - avatar (filr): Аватар пользователя.
        - username (str): Юзернейм пользователя.
        - phone_number (str): Номер телефона пользователя.
        - favorite_movies (ManyToManyField): Любимые фильмы пользователя.
        - movie_ratings (json): Оценки пользователя для фильмов.
        - created_at (datetime): Дата и время создания профиля.
        - updated_at (datetime): Дата и время последнего обновления профиля.
    """
    user = models.OneToOneField(
        verbose_name=_("User"),
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_profile",
    )
    birth_date = models.DateField('Birth Date', validators=[
                                  validate_age], blank=True, null=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', null=True,
                               blank=True)
    username = models.CharField(
        verbose_name='Username', max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(
        'Phone Number', blank=True, validators=[validate_phone_number])

    favorite_movies = models.ManyToManyField(verbose_name='Favorite Movies', to=Movie, related_name='favorites_people',
                                             blank=True)
    movie_ratings = models.JSONField(
        verbose_name='User Ratings', blank=True, null=True, default=dict())
    liked_movies = models.ManyToManyField(to=Movie, verbose_name='Liked Movies', blank=True,related_name='liked_by_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Возвращает представляения профиля пользователся в виде его эмейла

        """
        return f"{self.user.email}"
