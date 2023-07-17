from django import forms
from users.models import User


class LoginForm(forms.Form):
    """
    Класс формы входа пользователя.

    Поля:
        - email (EmailField): Поле для ввода адреса электронной почты.
        - password (CharField): Поле для ввода пароля.

    Метаданные:
        - model (Model): Класс модели пользователя.
        - fields (tuple): Кортеж полей формы.

    """

    email = forms.EmailField(help_text='Email')
    password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password')
