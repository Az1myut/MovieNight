from django.db import models
from django.contrib.postgres.fields import ArrayField
from actors.models import Actor
# Create your models here.


class Movie(models.Model):
    """
    Модель фильма
        - title (str): Заголовок фильма.
        - tmbd_id (int): ID фильма в TMBD.
        - original_language (str): Оригинальный язык фильма.
        - overview (str): Описание фильма.
        - popularity (float): Популярность фильма.
        - vote_average (float): Средняя оценка фильма.
        - vote_count (int): Количество голосов для фильма.
        - release_date (date): Дата релиза фильма.
        - is_released (bool): Был ли фильм уже выпущен.
        - actors (ManyToMany): Список актеров фильма.
        - runtime(int) : Длительность фильма
        -budjet(int): Бюджет фильма
        -genres(ManyToMany):Жанры Фильма
        -keywords(ManyToMany): Ключевые слова фильма
        -image(file): Постер фильма
        -actors_list(list) Список имен актеров фильма
    """
    title = models.CharField(verbose_name='Title', max_length=255)
    original_language = models.CharField(
        verbose_name='Oiginal Language', max_length=255)
    is_released = models.BooleanField(verbose_name='Released', default=False)
    release_date = models.DateField(verbose_name='Release Data')
    runtime = models.IntegerField(
        verbose_name='Runtime', blank=True, null=True)
    budjet = models.BigIntegerField(
        verbose_name='Budjet', blank=True, null=True)
    overview = models.TextField(
        verbose_name='Description', blank=True, null=True)
    popularity = models.FloatField(
        verbose_name='Popularity', null=True, blank=True)
    vote_average = models.FloatField(
        verbose_name='Average Vote', null=True, blank=True)
    vote_count = models.IntegerField(
        verbose_name='Count of Votes', null=True, blank=True)
    tmbd_id = models.BigIntegerField(verbose_name='TMBD ID')
    genres = models.ManyToManyField(
        to='Genre', verbose_name='Genres', related_name='genre_movies')
    keywords = models.ManyToManyField(
        to='Keyword', verbose_name='Keywords', related_name='keyword_movies')
    actors = models.ManyToManyField(
        to=Actor, verbose_name='Actors', related_name='actor_movies')
    image = models.ImageField(verbose_name='Image',
                              upload_to='movies/%d%m%Y', blank=True)
    actors_list = ArrayField(models.CharField(max_length=200), blank=True)
    likes_count = models.IntegerField(verbose_name='Like Count',default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-popularity', '-vote_average']

    def __str__(self):
        """
        Возвращает строковое представление объекта фильма в виде его названия

        """
        return f'{self.title}'


class Genre(models.Model):
    """
    Модель жанра 
        - name (str): Имя жанра.
        - genre_id (int): ID жанра в TMBD.

    """
    name = models.CharField(verbose_name='Name', max_length=255)
    genre_id = models.BigIntegerField(verbose_name='TMBD ID')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['genre_id',]

    def __str__(self):
        """
        Возвращает строковое представление объекта жанра в виде имени 


        """
        return f'{self.name}'


class Keyword(models.Model):
    """
    Модель жанра 
        - name (str): Имя ключевого слова.
        - keyword_id (int): ID ключевого слова в TMBD.

    """
    name = models.CharField(verbose_name='Name', max_length=255)
    keyword_id = models.BigIntegerField(verbose_name='TMBD ID')

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'
        ordering = ['keyword_id',]

    def __str__(self):
        """
        Возвращает строковое представление объекта жанра в виде имени 


        """
        return f'{self.name}'
