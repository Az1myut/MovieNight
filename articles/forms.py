from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """
    Форма для создания и редактирования статьи.

    Атрибуты:
        title (str): Поле для ввода заголовка статьи.
        image (file): Поле для загрузки изображения к статье.

    Вложенный класс Meta:
        model (Article): Модель, с которой связана форма.
        fields (list): Список полей модели, отображаемых в форме.
        widgets (dict): Словарь виджетов для настройки отображения полей формы.

    """
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Title',
                                                          'style': 'max-width: 400px;', }))
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control-file'
                                                           }))

    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 600px; resize:none',
                'placeholder': 'Your content',
                'rows': 20,
                'cols': 50,

            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'resize:none;',
                'placeholder': 'Comment',
                'rows': 5,
                'cols': 5,

            }),
        }