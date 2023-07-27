from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, UserProfile
from phone_field import PhoneField
from .validators import validate_phone_number, validate_age


class CustomUserCreationForm(UserCreationForm):
    """
    Пользовательская форма создания пользователя наследуемая от UserCreationForm
    """
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """
    Пользовательская форма изменения пользователя наследуемая от UserChangeForm
    """
    class Meta:
        model = User
        fields = ("email",)


class UserProfileForm(forms.ModelForm):
    """
    Форма профиля пользователя.

    Поля:
        username(str) - Юзернейм профиля пользователя
        birth_date(date) - Дата пождения пользователя
        phone_number(str) - Телефонный номер пользователя
        avatar(file) - Аватарка  пользователя
    """
    username = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             'style': 'max-width: 300px;', }))
    birth_date = forms.DateField(required=False, validators=[validate_age])
    phone_number = forms.CharField(required=False, validators=[validate_phone_number],
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Phone Number'}))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={'class': 'form-control-file'
                                                            }))

    class Meta:
        model = UserProfile
        fields = ['username', 'avatar', 'phone_number', 'birth_date']


class UserForm(forms.ModelForm):
    """
    Форма пользователя 

    Поля:
        email(email) - Эмейл пользователя
    """
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Email',
                                                                          'style': 'max-width: 300px;'}))

    class Meta:
        model = User
        fields = ['email']
class EmailForm(forms.Form):
    """
    Форма пользователя 

    Поля:
        email(email) - Эмейл пользователя
    """
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Email',
                                                                          'style': 'max-width: 300px;'}))
