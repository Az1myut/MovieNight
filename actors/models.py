from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Gender(models.IntegerChoices):
    """
    Класс представляющий числовую выборку пола

    Атрибуты:
    NOT_SET(int) - не известно
    FEMALE(int) - женщина
    MALE(int) - мужчина
    NON_BINARY(int) - нет пола

    """
    NOT_SET = 0, _("Not Set")
    FEMALE = 1, _("Female")
    MALE = 2, _('Male')
    NON_BINARY = 3, _('Non Binary')


class Actor(models.Model):
    """
    Модель представляющая данные об актере

    Поля:
        name(str) - имя актера
        actor_id(int) - айди актера в базе tmbd
        gender(int) - число представляющее пол актера
        birth_data(date) - дата рождения актера
        image(file) - фото актера
        populariry(float) - популярность актера в числовом виде
        birth_place(str) - место рождения актера
        biography(str) - биография актера
    """
    name = models.CharField(verbose_name='Fullname', max_length=255)
    actor_id = models.BigIntegerField(verbose_name='Actor ID')
    gender = models.SmallIntegerField(
        verbose_name='Gender', choices=Gender.choices, default=Gender.NOT_SET)
    birth_date = models.DateField(
        verbose_name='Birth Date', blank=True, null=True)
    image = models.ImageField(verbose_name='Avatar',
                              upload_to='actors/%d%m%Y', blank=True, null=True)
    popularity = models.FloatField(
        verbose_name='Popularity', blank=True, null=True)
    birth_place = models.CharField(
        verbose_name='Birth Place', max_length=255, blank=True, null=True)
    biography = models.TextField(
        verbose_name='Biography', blank=True, null=True)

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'
        ordering = ['-popularity', 'birth_date']

    def __str__(self):
        """
        Возвращает представляения актера в виде его имени

        """
        return f'{self.name}'
