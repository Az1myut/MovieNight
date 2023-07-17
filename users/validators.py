from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_age(value):
    """
    Проверяет возраст пользователя.

    Параметры:
        - value (date): Дата рождения пользователя.

    Rasises:
        - ValidationError: Если возраст пользователя меньше 12 лет.
    """
    age = abs((timezone.now().date() - value)).days

    if age < (12 * 365):
        raise ValidationError('Вам должно быть от 12 лет.')


def validate_phone_number(phone_number):
    """
    Проверяет номер телефона пользователя.

    Параметры:
        - phone_number (str): Номер телефона пользователя.

    Raises:
        - ValidationError: Если номер телефона содержит недопустимые символы.
        - ValidationError: Если длина номера телефона не равна 12 символам.
        - ValidationError: Если номер телефона не начинается с 998.
    """
    for number in phone_number:
        if number not in ('1234567890'):
            raise ValidationError(
                ('Phone Number must have only digits'),
                params={'phone_number': phone_number},
            )
    if len(phone_number) != 12:
        raise ValidationError(
            ('Phone number in Uzbekistan must have 12 digits'))
    if phone_number[0:3] != '998':
        raise ValidationError(
            ('Phone number  in Uzbekistan must start with 998'))
