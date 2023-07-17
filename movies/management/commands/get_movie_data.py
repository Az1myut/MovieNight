import time
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
import os
from datetime import date
import requests
from pathlib import Path
from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand
from icecream import ic
from movies.models import (
    Movie,
    Genre,
    Keyword,
)


@sync_to_async
def create_movie(title, tmbd_id, original_language, overview,
                 popularity, vote_average, vote_count,
                 release_date, is_released, actors):
    """
    Создает объект фильма и добавляет его в базу данных.

    Параметры:
        - title (str): Заголовок фильма.
        - tmbd_id (int): ID фильма в TMBD.
        - original_language (str): Оригинальный язык фильма.
        - overview (str): Описание фильма.
        - popularity (float): Популярность фильма.
        - vote_average (float): Средняя оценка фильма.
        - vote_count (int): Количество голосов для фильма.
        - release_date (date): Дата релиза фильма.
        - is_released (bool): Был ли фильм уже выпущен.
        - actors (list): Список актеров фильма.

    Возвращает:
        - new_movie (Movie): Созданный объект фильма.
    """
    new_movie = Movie.objects.create(title=title, tmbd_id=tmbd_id, original_language=original_language,
                                     overview=overview, popularity=popularity, vote_average=vote_average,
                                     vote_count=vote_count, release_date=release_date, is_released=is_released,
                                     actors_list=actors)
    return new_movie


@sync_to_async
def keyword_get_or_create(movie_instance, name, keyword_id):
    """
    Получает или создает объект ключевого слова для фильма и связывает его с фильмом.

    Параметры:
        - movie_instance (Movie): Объект фильма.
        - name (str): Название ключевого слова.
        - keyword_id (int): ID ключевого слова в tmbd

    Возвращает:
        - movie_instance (Movie): Обновленный объект фильма.
    """
    keyword_object, created = Keyword.objects.get_or_create(
        name=name, keyword_id=keyword_id)
    if created:
        movie_instance.keywords.add(keyword_object)
    else:
        if keyword_object in movie_instance.keywords.all():
            pass
        movie_instance.keywords.add(keyword_object)
    return movie_instance


@sync_to_async
def movie_image_save(movie_instance, filename, filepath):
    """
    Сохраняет изображение фильма и добавляет его к объекту фильма.

    Параметры:
        - movie_instance (Movie): Объект фильма.
        - filename (str): Имя файла изображения.
        - filepath (str): Путь к файлу изображения.

    Возвращает:
        - movie_instance (Movie): Обновленный объект фильма.
    """
    movie_instance.image.save(filename, File(open(filepath, 'rb')))

    os.remove(filepath)

    movie_instance.save()
    return movie_instance


class Command(BaseCommand):
    """
    Django команда для получения данных фильма.
    """
    help = 'Get Movie Data'

    async def retrieve_data(self, url):
        """
        Асинхронно получает данные фильма из удаленного API.

        Параметры:
            - url (str): URL для получения данных фильма.

        Возвращает:
            - data (dict): Полученные данные фильма.
        """
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNTdmMmY4ZTgzN2RiNTkxZGY5MjJiMmE0NDJiODI2MCIsInN1YiI6IjY0OTMzOWRjZDIxNDdjMDEzOWNhNTk3OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.joP5hGXke4soHfVgQ999XFM84W4WRagl_1dG1fAeE2o"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data

    async def set_released_status(self, release_date):
        """
        Асинхронно устанавливает статус "выпущен" в зависимости от даты релиза фильма.

        Параметры:
            - release_date (date): Дата релиза фильма.

        Возвращает:
            - status (bool): Статус "выпущен".
        """
        if release_date <= date.today():
            status = True
        else:
            status = False
        return status

    async def set_release_date(self, release_date):
        """
        Асинхронно устанавливает дату релиза фильма.

        Параметры:
            - release_date (str): Дата релиза фильма (формат: "YYYY-MM-DD").

        Возвращает:
            - released_date (date): Объект даты релиза фильма.
        """

        released_date = release_date.split('-')

        year = int(released_date[0])
        month = int(released_date[1])
        day = int(released_date[2])
        released_date = date(year=year, month=month, day=day)
        return released_date

    async def get_image(self, image_url):
        """
        Асинхронно получает изображение фильма по заданному URL.

        Параметры:
            - image_url (str): URL изображения фильма.

        Возвращает:
            - response (aiohttp.client_reqrep.ClientResponse): Ответ с загруженными данными изображения.
            - full_image_url (str): Полный URL изображения фильма.
        """
        full_image_url = f'https://image.tmdb.org/t/p/w500{image_url}'
        async with aiohttp.ClientSession() as session:
            async with session.get(full_image_url) as response:
                return response, full_image_url

    async def add_image(self, image_url):
        """
        Асинхронно загружает изображение фильма и сохраняет его в файловой системе.

        Параметры:
            - image_url (str): URL изображения фильма.

        Возвращает:
            - (filename, file_path): Имя и путь к сохраненному файлу изображения.
        """
        full_image_url = f'https://image.tmdb.org/t/p/w500{image_url}'
        response = requests.get(full_image_url)
        filename = os.path.basename(full_image_url)
        file_path = Path(settings.MEDIA_MOVIES_ROOT, filename)
        with open(file_path, 'wb') as destination:
            destination.write(response.content)
        return (filename, file_path)

    async def get_actors(self, tmbd_id):
        """
    Асинхронно получает список актеров для фильма с заданным ID из удаленного API.

    Параметры:
        - tmbd_id (int): ID фильма в TMBD.

    Возвращает:
        - result (dict): Результат запроса с данными актеров фильма.
    """
        url = f'https://api.themoviedb.org/3/movie/{tmbd_id}/credits?language=en-US'
        result = await self.retrieve_data(url)
        return result

    async def add_actors(self, tmbd_id):
        """
    Асинхронно добавляет актеров фильма с заданным ID в список актеров фильма.

    Параметры:
        - tmbd_id (int): ID фильма в TMBD.

    Возвращает:
        - actors_list (list): Список актеров фильма.
        """
        result = await(self.get_actors(tmbd_id=tmbd_id))
        cast = result.get('cast')
        actors_list = []
        for person in cast:
            if person['known_for_department'] == 'Acting':
                name = person['name']
                character = person['character']
                name_character = f'{name}-{character}'
                actors_list.append(name_character)
        return actors_list

    @sync_to_async
    def add_genres(self, movie_instance, genre_ids):
        """
        Асинхронно добавляет жанры фильма к объекту фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.
            - genre_ids (list): Список ID жанров фильма.

        Возвращает:
            - movie_instance (Movie): Обновленный объект фильма.
        """
        for genre_id in genre_ids:
            genre = Genre.objects.get(genre_id=genre_id)
            movie_instance.genres.add(genre)
        return movie_instance

    async def get_keywords(self, tmbd_id):
        """
            Асинхронно получает ключевые слова для фильма с заданным ID из удаленного API.

            Параметры:
                - tmbd_id (int): ID фильма в TMBD.

            Возвращает:
                - result (dict): Результат запроса с ключевыми словами фильма.
        """
        url = f"https://api.themoviedb.org/3/movie/{tmbd_id}/keywords"
        result = await self.retrieve_data(url)
        return result

    async def add_keywords(self, movie_instance, tmbd_id):
        """
    Асинхронно добавляет ключевые слова фильма к объекту фильма.

    Параметры:
        - movie_instance (Movie): Объект фильма.
        - tmbd_id (int): ID фильма в TMBD.

    Возвращает:
        - movie_instance (Movie): Обновленный объект фильма.
    """
        result = await self.get_keywords(tmbd_id=tmbd_id)
        keywords = result.get('keywords')
        for keyword in keywords:
            keyword_id = keyword['id']
            name = keyword['name']
            movie_instance = await keyword_get_or_create(movie_instance=movie_instance, name=name, keyword_id=keyword_id)
        return movie_instance

    async def create_movies(self, movies):
        """
        Асинхронно создает и сохраняет объекты фильмов.


        Параметры:
            - movies (list): Список данных фильмов.
        """
        for movie in movies:
            movie_lst = []
            async for movie in Movie.objects.filter(tmbd_id=movie['id']):
                movie_lst.append(movie)

            if len(movie_lst) == 0:
                title = movie['title']
                tmbd_id = movie['id']
                original_language = movie['original_language']
                overview = movie['overview']
                popularity = movie['popularity']
                vote_average = movie['vote_average']
                vote_count = movie['vote_count']
                if movie['release_date'] == '':
                    continue
                release_date = await self.set_release_date(
                    release_date=movie['release_date'])
                is_released = await self.set_released_status(
                    release_date=release_date)
                actors = await self.add_actors(tmbd_id=tmbd_id)

                new_movie = await create_movie(title=title, tmbd_id=tmbd_id, original_language=original_language,
                                               overview=overview, popularity=popularity, vote_average=vote_average,
                                               vote_count=vote_count, release_date=release_date, is_released=is_released,
                                               actors_list=actors)
                new_movie = await self.add_genres(movie_instance=new_movie, genre_ids=movie['genre_ids'])

                new_movie = await self.add_keywords(movie_instance=new_movie, tmbd_id=tmbd_id)
                if movie['poster_path'] is None:
                    continue
                filename, filepath = await self.add_image(image_url=movie['poster_path'])

                await movie_image_save(movie_instance=new_movie, filename=filename, filepath=filepath)

    async def main(self):
        """
        Асинхронная функция для выполнения основной логики команды.
        В которой мы получаем через реквест в базу tmbd список фильмов
        """
        for number in range(20, 41):
            url_for_rated_movies = f'https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={number}'
            url_for_popular_movies = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={number}"
            url_for_upcoming_movies = f"https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={number}"
            url_for_week_trending_movies = f'https://api.themoviedb.org/3/trending/movie/week?language=en-US&page={number}'
            url_for_now_playing_movies = f'https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={number}'
            result = await self.retrieve_data(url_for_now_playing_movies)
            movies = result.get('results')
            print(number)

            await self.create_movies(movies=movies)

    def handle(self, *args, **kwargs):
        """
        Обрабатывает команду.
        Запускает основную функцию main
        """
        start_time = time.time()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

        print("--- %s seconds ---" % (time.time() - start_time))
