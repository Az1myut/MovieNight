from django.db import models
from phone_field import PhoneField
# Create your models here.
from django.db import models

# Create your models here.


class ContactPage(models.Model):
    """
    Модель страницы контактов.

    Поля:
        - adress (str): Адрес контактов
        - phone (str): Телефон контактов
        - email (email): Email контактов
        - website (str): Веб-сайт контактов
        - info (str): Информация контактов


    Методы:
        - __str__() -> str: Возвращает строковое представление модели.
    """
    adress = models.CharField(verbose_name='Adress', max_length=50)
    phone = PhoneField(verbose_name='Phone', max_length=50)
    email = models.EmailField(verbose_name='Email')
    website = models.CharField(verbose_name='Web Site', max_length=50)
    info = models.TextField(verbose_name='Information')

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self) -> str:
        """
        Возвращает строковое представление модели
        В виде адреса и телефона
        """
        return f'{self.adress} - {self.phone}'


class ContactMessage(models.Model):
    """
    Модель сообщения .

    Поля:
        - name (CharField): Полное имя отправителя сообщения
        - email (EmailField): Email отправителя сообщения
        - subject (CharField): Тема сообщения
        - message (TextField): Контент сообщения



    Методы:
        - __str__() -> str: Возвращает строковое представление модели.
    """

    name = models.CharField(verbose_name='Full Name', max_length=50)
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(verbose_name='Subject', max_length=100)
    message = models.TextField(verbose_name='Message')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self) -> str:
        """
        Возвращает строковое представление сообщения в виде темы сообщения.
        """
        return f'{self.subject}'
