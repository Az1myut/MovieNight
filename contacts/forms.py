from django import forms
from .models import ContactMessage

from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField
from icecream import ic
from django.utils.translation import gettext_lazy as _


class ContactMessageForm(forms.ModelForm):
    """
    Форма для модели ContactMessage.


    Эта форма используется для создания или редактирования объектов модели ContactMessage.

    Атрибуты:
        captcha (CaptchaField): Поле для капчи (CAPTCHA).

    Мета-класс:
        model (Model): Модель, с которой связана форма.
        fields (list или '__all__'): Поля модели, отображаемые в форме.
        widgets (dict): Виджеты для полей модели, определяющие их отображение и атрибуты.

    """
    captcha = CaptchaField(label="Solve Math Problem")

    class Meta:
        model = ContactMessage
        fields = '__all__'
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Subject'
            }),
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Your Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Type Your Message'
            }),
        }
