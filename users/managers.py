from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.

    Методы:
        _create_user() - Создает и сохраняет нового пользователя
        create_user() - Создает и сохраняет нового обычного пользователя.
        create_superuser() -  Создает и сохраняет нового суперпользователя
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Создает и сохраняет нового пользователя.

        Параметры:
            - email (str): Email пользователя.
            - password (str): Пароль пользователя.
            - is_staff (bool): Является ли пользователь сотрудником.
            - is_superuser (bool): Является ли пользователь суперпользователем.
            - **extra_fields: Дополнительные атрибуты пользователя.

        Возвращает:
            - user (User): Созданный пользователь.
        """
        if not email:
            raise ValueError('Email must be set')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет нового обычного пользователя.

        Параметры:
            - email (str): Email пользователя.
            - password (str): Пароль пользователя.
            - **extra_fields: Дополнительные атрибуты пользователя.

        Возвращает:
            - user (User): Созданный обычный пользователь.
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет нового суперпользователя.

        Параметры:
            - email (str): Email пользователя.
            - password (str): Пароль пользователя.
            - **extra_fields: Дополнительные атрибуты пользователя.

        Возвращает:
            - user (User): Созданный суперпользователь.
        """
        user = self._create_user(email, password, True, True, is_moderator = True,**extra_fields)
        user.save(using=self._db)
        return user
