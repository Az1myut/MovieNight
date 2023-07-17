from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User
from icecream import ic


class UserSerialzer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.

    Метаданные:
        - model (Model): Класс модели пользователя.
        - fields (list): Список полей сериализатора.
        - extra_kwargs (dict): Дополнительные аргументы для полей.

    Методы:
        - create(validated_data) -> User: Создает новый экземпляр пользователя.
        - validate_password(value) -> str: Проверяет и возвращает валидный пароль.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает новый экземпляр пользователя.

        Аргументы:
            - validated_data (dict): Проверенные данные.

        Возвращает:
            User: Созданный экземпляр пользователя.
        """
        password = validated_data.pop('password', None)
        ic(password)
        instance = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        ic(instance.password)
        instance.save()
        return instance

    def validate_password(self, value):
        """
        Проверяет и возвращает валидный пароль.

        Аргументы:
            - value (str): Пароль для проверки.

        Возвращает:
            str: Валидный пароль.
        """
        
        validate_password(value)

        return value
