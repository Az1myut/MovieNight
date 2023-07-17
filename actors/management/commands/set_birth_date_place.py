import time
from datetime import date
import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from django.db.models import Q
from django.core.management.base import BaseCommand
from icecream import ic
from movies.models import (
    Movie,
)
from actors.models import (
    Actor
)


@sync_to_async
def save_actor_instance(actor_instance):
    """
    Асинхронно сохраняет экземпляр актера.

    Аргументы:
        actor_instance (Actor): Экземпляр актера для сохранения.

    Возвращает:
        Actor: Сохраненный экземпляр актера.
    """
    actor_instance.save()
    return actor_instance


@sync_to_async
def get_actors_list():
    """
    Асинхронно получает список актеров бу которых даты рождения и места рождения None.

    Возвращает:
        list: Список экземпляров актеров.
    """
    actors_list = []
    query = Q(birth_date=None) & Q(birth_place=None)
    actors = Actor.objects.filter(query)
    for actor in actors:
        actors_list.append(actor)
    return actors_list


class Command(BaseCommand):
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

    async def set_birth_date(self, birth_date):
        """
        Асинхронно преобразует строку даты рождения в объект datetime.date.

        Аргументы:
            birth_date (str): Строка даты рождения.

        Возвращает:
            date: Дата рождения в виде объекта date.
        """
        birth_datee = birth_date.split('-')
        year = int(birth_datee[0])
        month = int(birth_datee[1])
        day = int(birth_datee[2])
        birth_datee = date(year=year, month=month, day=day)
        return birth_datee

    async def actor_set_birth_date_place(self, actor_instance, result):
        """
        Асинхронно устанавливает дату рождения, место рождения и пол для экземпляра актера.

        Аргументы:
            actor_instance (Actor): Экземпляр актера.
            result (dict): Данные, содержащие сведения об актере.

        Возвращает:
            actor_instance (Actor): Обновленный экземпляр актера.
        """
        birth_date = result.get('birthday')
        if birth_date:
            birth_date = await self.set_birth_date(birth_date=birth_date)

            actor_instance.birth_date = birth_date
        birth_place = result.get('place_of_birth')
        if birth_place:
            actor_instance.birth_place = birth_place

        gender = result.get('gender')
        if gender:
            actor_instance.gender = gender

        actor_instance = await save_actor_instance(actor_instance=actor_instance)
        return actor_instance

    async def main(self):
        """
        Основная асинхронная функция для получения даты рождения, места рождения и пола
        получаем сначала актеров у кого место и дата рождения None
        пробегамся по актерам и получаем их данные через запрос в базу tmbd 
        получив данные обновляем актера
        """
        num = 0
        actors = await get_actors_list()
        for actor in actors:

            actor_url = f'https://api.themoviedb.org/3/person/{actor.actor_id}?language=en-US'
            result = await self.retrieve_data(url=actor_url)

            actor = await self.actor_set_birth_date_place(actor_instance=actor, result=result)

            num += 1
            ic(num)
    help = 'Get Actors Bith Date Place'

    def handle(self, *args, **kwargs):
        """
        Основная функция для запуска команды
        Внутри ней мы засекаем время и запускаем основную  асинхронную функцию для обновления актеров.
        """
        start_time = time.time()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.main())

        print("--- %s seconds ---" % (time.time() - start_time))
