import time
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from icecream import ic
from movies.models import (
    Genre,
)


class Command(BaseCommand):
    """
    Команда для создания жанров.

    Атрибуты:
        - help (str): Справка о команде.

    Методы:
        - create_genres(genres: List[dict]): Создает жанры на основе предоставленных данных.
        - handle(*args, **kwargs): Обрабатывает команду.
    """
    help = 'Create Genres'

    def create_genres(self, genres):
        """
        Создает жанры на основе предоставленных данных.

        Аргументы:
            - genres (List[dict]): Список словарей с данными о жанрах.
        """
        for genre in genres:
            if len(Genre.objects.filter(genre_id=int(genre['id']))) == 0:
                new_genre = Genre.objects.create(
                    name=genre['name'], genre_id=int(genre['id']))
                new_genre.save()
            else:
                continue

    def handle(self, *args, **kwargs):
        """
        Обрабатывает команду.
        Делает запрос в базу tmbd берет данные о жанрах, с помощью данных создает жанры

        Аргументы:
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.
        """
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNTdmMmY4ZTgzN2RiNTkxZGY5MjJiMmE0NDJiODI2MCIsInN1YiI6IjY0OTMzOWRjZDIxNDdjMDEzOWNhNTk3OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.joP5hGXke4soHfVgQ999XFM84W4WRagl_1dG1fAeE2o"
        }
        start_time = time.time()
        url = f"https://api.themoviedb.org/3/genre/movie/list?language=en"
        resp = requests.get(url, headers=headers)
        result = resp.json()
        genres = result.get('genres')
        self.create_genres(genres=genres)

        print("--- %s seconds ---" % (time.time() - start_time))
