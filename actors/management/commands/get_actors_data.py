import time
import aiohttp
import asyncio
import requests
from asgiref.sync import sync_to_async
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from icecream import ic
from movies.models import (
    Movie,
)
from actors.models import (
    Actor
)


@sync_to_async
def actor_exists(fullname):
    """
    Проверяет, существует ли актер с данным именем в базе данных.

    Аргументы:
        fullname (str): Полное имя актера.

    Возвращает:
        bool: True, если актер существует в базе данных, в противном случае False.
    """
    actors = Actor.objects.filter(name=fullname)
    if len(actors) == 0:
        return False
    else:
        return True


@sync_to_async
def fullname_consists_two_names(fullname):
    """
    Проверяет, состоит ли полное имя актера из двух частей (имени и фамилии).

    Аргументы:
        fullname (str): Полное имя актера.

    Возвращает:
        bool: True, если полное имя состоит из двух частей, если из одной части то False
    """
    names = fullname.split(' ')
    if len(names) == 2:
        return True
    elif len(names) == 1:
        return False


@sync_to_async
def pre_create_actor(name, actor_id):
    """
    Создает экземпляр актера с предварительным заполнением имени и его  айди в базе tmbd 

    Аргументы:
        name (str): Имя актера.
        actor_id (int): айди в базе tmbd 

    Возвращает:
        Actor: Экземпляр созданного актера.
    """
    actor_instance = Actor.objects.create(name=name, actor_id=actor_id)
    return actor_instance


@sync_to_async
def actor_image_save(actor_instance, filename, filepath):
    """
    Сохраняет изображение актера.

    Аргументы:
        actor_instance (Actor): Экземпляр актера.
        filename (str): Имя файла.
        filepath (str): Путь к файлу.

    Возвращает:
        Actor: Экземпляр актера.
    """
    actor_instance.image.save(filename, File(open(filepath, 'rb')))
    return actor_instance


@sync_to_async
def save_actor_instance(actor_instance):
    """
    Сохраняет экземпляр актера.

    Аргументы:
        actor_instance (Actor): Экземпляр актера.

    Возвращает:
        Actor: Экземпляр актера.
    """
    actor_instance.save()
    return actor_instance


@sync_to_async
def get_actor_instance(fullname):
    """
    Возвращает экземпляр актера по полному имени.

    Аргументы:
        fullname (str): Полное имя актера.

    Возвращает:
        Actor: Экземпляр актера или None, если актер не найден.
    """
    actor_instance = Actor.objects.filter(name=fullname).first()
    return actor_instance


@sync_to_async
def get_movies_list():
    """
    Возвращает список фильмов, у которых отсутствуют связанные актеры.

    Возвращает:
        list: Список фильмов.
    """
    movies_list = []
    movies = Movie.objects.filter(actors=None)
    for movie in movies:
        movies_list.append(movie)
    return movies_list


@sync_to_async
def movie_set_actors(movie_instance, actor_instances_list):
    """
    Связывает список актеров с фильмом.

    Аргументы:
        movie_instance (Movie): Экземпляр фильма.
        actor_instances_list (list): Список экземпляров актеров.

    Возвращает:
        Movie: Экземпляр фильма.
    """

    movie_instance.actors.set(actor_instances_list)

    return movie_instance


class Command(BaseCommand):
    """
    Команда для получения данных об актерах с базы tmbd.
    """
    async def retrieve_data(self, url):
        """
        Асинхронно получает данные по указанному URL.

        Аргументы:
            url (str): URL для получения данных.

        Возвращает:
            dict: Полученные данные в виде словаря.
        """
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNTdmMmY4ZTgzN2RiNTkxZGY5MjJiMmE0NDJiODI2MCIsInN1YiI6IjY0OTMzOWRjZDIxNDdjMDEzOWNhNTk3OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.joP5hGXke4soHfVgQ999XFM84W4WRagl_1dG1fAeE2o"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data

    async def add_image(self, image_url):
        """
        Асинхронно добавляет изображение.

        Аргументы:
            image_url (str): URL изображения.

        Возвращает:
            tuple: Кортеж, содержащий имя файла и путь к сохраненному изображению.
        """
        full_image_url = f'https://image.tmdb.org/t/p/w500{image_url}'
        response = requests.get(full_image_url)
        filename = os.path.basename(full_image_url)
        file_path = Path(settings.MEDIA_ROOT, filename)

        with open(file_path, 'wb') as destination:
            destination.write(response.content)
        return (filename, file_path)

    async def set_actor_details(self, actor_instance, result):
        """
        Асинхронно устанавливает поля актера.

        Аргументы:
            actor_instance (Actor): Экземпляр актера.
            result (dict): Данные, содержащие данные об актере.

        Возвращает:
            Actor: Обновленный экземпляр актера.
        """
        if result.get('birth_date'):
            birth_day = result['birth_date']
            actor_instance.birth_date = birth_day
        if result.get('popularity'):
            popularity = result['popularity']
            actor_instance.popularity = popularity
        if result.get('birth_place'):
            birth_place = result['birth_place']
            actor_instance.birth_place = birth_place
        if result.get('biography'):
            biography = result['biography']
            actor_instance.biography = biography
        if result.get('profile_path'):
            profile_path = result['profile_path']
            if 'None' not in profile_path:
                filename, file_path = await self.add_image(image_url=profile_path)
                actor_instance = await actor_image_save(actor_instance=actor_instance, filename=filename, filepath=file_path)
        return actor_instance

    async def create_actor(self, actor_id):
        """
        Асинхронно создает актера с помощью полученных данных с запроса.

        Аргументы:
            actor_id (int): Идентификатор актера.

        Возвращает:
            Actor: Созданный экземпляр актера.
        """
        url = f'https://api.themoviedb.org/3/person/{actor_id}?language=en-US'
        result = await self.retrieve_data(url)
        name = result['name']
        actor_instance = await pre_create_actor(name=name, actor_id=actor_id)

        actor_instance = await self.set_actor_details(actor_instance=actor_instance, result=result)

        actor_instance = await save_actor_instance(actor_instance=actor_instance)
        return actor_instance

    async def get_actor_instances(self, actors_list):
        """
        Асинхронно получает список экземпляров актеров.
        Идет прохождения по 10 именам в списке актеров, делается запрос в базу tmbd по нахождению актера,
        если нет результатов, то переходим к следующему имени,если актер нашелся, то проверяем находится ли он
        в нашей базе данных, е
        Если находится:
            то про добавляем в список экземпляров актеров
        Если нет:
            то создаем его и добавляем с спиок
        Аргументы:
            actors_list (list): Список имен актеров.

        Возвращает:
            list: Список экземпляров актеров.
        """
        actor_instances_list = []
        actors_list = actors_list[:10]
        for actor_character in actors_list:

            fullname = actor_character.split('-')[0]

            if await fullname_consists_two_names(fullname=fullname):
                first_name = fullname.split(' ')[0]
                last_name = fullname.split(' ')[1]
                search_actor_url = f'https://api.themoviedb.org/3/search/person?query={first_name}%20{last_name}\
                                &include_adult=false&language=en-US&page=1'
            else:
                name = fullname.split(' ')[0]
                search_actor_url = f'https://api.themoviedb.org/3/search/person?query={name}\
                                &include_adult=false&language=en-US&page=1'
            result = await self.retrieve_data(url=search_actor_url)
            if result['results'] == []:
                continue
            actor_id = result['results'][0]['id']
            if await actor_exists(fullname=fullname):
                actor_instance = await get_actor_instance(fullname=fullname)
            else:
                actor_instance = await self.create_actor(actor_id=actor_id)

            actor_instances_list.append(actor_instance)
        return actor_instances_list

    async def main(self):
        """
        Основная асинхронная функция для добваления актеров  фильмам.
        Получаем фильмы где нет еще связанных актеров, пробегаемся по фильмам
        заполняем списиок экземпляров актеров для одного фильма с помощью списка имен актеров,
        потом связываем экземпляры актеров с фильмом 
        """
        num = 0
        movies = await get_movies_list()
        for movie in movies:
            actors_list = movie.actors_list
            actor_instances_list = await self.get_actor_instances(actors_list=actors_list)
            await movie_set_actors(movie_instance=movie, actor_instances_list=actor_instances_list)
            num += 1
    help = 'Get Actors Data'

    def handle(self, *args, **kwargs):
        """
        Основная функция для запуска команды
        Внутри ней мы засекаем время и запускаем основную  асинхронную функцию для добваления актеров  фильмам.
        """
        start_time = time.time()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

        print("--- %s seconds ---" % (time.time() - start_time))
