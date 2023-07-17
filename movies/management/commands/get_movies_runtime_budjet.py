import time
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from icecream import ic
from movies.models import (
    Movie,
)


@sync_to_async
def movie_save(movie_instance):
    """
    Асинхронно сохраняет экземпляр фильма.

    Аргументы:
        - movie_instance (Movie): Экземпляр фильма.
    """
    movie_instance.save()


@sync_to_async
def get_movies_list():
    """
    Асинхронно получает список фильмов.

    Возвращает:
        List[Movie]: Список экземпляров фильмов.
    """
    movies_list = []
    movies = Movie.objects.all()
    for movie in movies:
        movies_list.append(movie)
    return movies_list


class Command(BaseCommand):
    """
    Команда для получения информации о длительности и бюджете фильмов.

    Методы:
        - retrieve_data(url: str) -> dict: Асинхронно получает данные по заданному URL.
        - set_runtime_budjet(movie_instance: Movie, result: dict): Устанавливает длительность и бюджет фильма на основе полученных данных.
        - main(): Основной асинхронный метод для получения информации о длительности и бюджете фильмов.
        - handle(*args, **kwargs): Обрабатывает команду.
    """
    async def retrieve_data(self, url):
        """
        Асинхронно получает данные по заданному URL.

        Аргументы:
            - url (str): URL для получения данных.

        Возвращает:
            dict: Полученные данные.
        """
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNTdmMmY4ZTgzN2RiNTkxZGY5MjJiMmE0NDJiODI2MCIsInN1YiI6IjY0OTMzOWRjZDIxNDdjMDEzOWNhNTk3OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.joP5hGXke4soHfVgQ999XFM84W4WRagl_1dG1fAeE2o"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data

    async def set_runtime_budjet(self, movie_instance, result):
        """
        Устанавливает длительность и бюджет фильма на основе полученных данных.
        Если длительность и бюджет фильма равны None или 0 то 
        длительность и бюджет фильма не устанваливаются

        Аргументы:
            - movie_instance (Movie): Экземпляр фильма.
            - result (dict): Полученные данные.

        """
        runtime, budget = False, False
        if result.get('runtime'):
            if result['runtime'] != 0 or result['runtime'] is not None:
                runtime = result['runtime']
        if result.get('budget'):
            if result['budget'] != 0 or result['budget'] is not None:
                budget = result['budget']
        if runtime:
            movie_instance.runtime = runtime
        if budget:
            movie_instance.budjet = budget
        await movie_save(movie_instance=movie_instance)

    async def main(self):
        """
        Основной асинхронный метод для получения информации о длительности и бюджете фильмов.
        Пробегаемся по списку фильмов и для каждого фильма делаем запрос в базу tmbd

        =
        """
        movies = await get_movies_list()
        for movie in movies:
            movie_id = movie.tmbd_id
            url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            result = await self.retrieve_data(url)
            await self.set_runtime_budjet(movie_instance=movie, result=result)
            ic(movie_id)
    help = 'Get Runtime and Budjet'

    def handle(self, *args, **kwargs):
        """
        Обрабатывает команду. В которой вызывается метод main

        Аргументы:
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.
        """
        start_time = time.time()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

        print("--- %s seconds ---" % (time.time() - start_time))
