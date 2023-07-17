from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Actor, Gender
# Create your views here.


class ShowActorPageDetailView(DetailView):
    """
    Контроллер класса  для отображения подробной информации об актере.

    Атрибуты:
        context_object_name (str): Имя переменной для объекта актера в шаблоне.
        model (django.db.models.Model): Класс модели, представляющий актера.
        template_name (str): Имя шаблона, используемого для отображения страницы с подробной информацией об актере.

    Методы:
        get_birth_date: Возвращает дату рождения актера, если она доступна, в противном случае None.
        get_popularity: Возвращает популярность актера, если она доступна, в противном случае 'Неизвестно'.
        get_biography: Возвращает биографию актера, если она доступна, в противном случае 'Нет биографии для данного актера'.
        get_birth_place: Возвращает место рождения актера, если оно доступно, в противном случае 'Неизвестно'.
        get_image: Возвращает URL изображения актера, если оно доступно, в противном случае None.
        get_gender: Возвращает пол актера, если он доступен, в противном случае 'Неизвестно'.
        get_actor_movies: Возвращает фильмы, связанные с актером.
        get_context_data: Метод чтобы добавить  данные контекста для отображения шаблона.

    """
    context_object_name = 'actor'
    model = Actor
    template_name = 'actors/actor_detail.html'

    def get_birth_date(self, actor_instance):
        """
        Возвращает дату рождения актера, если она доступна, в противном случае None.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            date или None: Дата рождения актера или None.
        """
        birth_date = actor_instance.birth_date
        if birth_date:
            return birth_date
        else:
            return None

    def get_popularity(self, actor_instance):
        """
        Возвращает популярность актера, если она доступна, в противном случае 'Неизвестно'.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            float или str: Популярность актера или 'Неизвестно'.
        """
        popularity = actor_instance.popularity
        if popularity:
            return popularity
        else:
            return 'Unknown'

    def get_biography(self, actor_instance):
        """
        Возвращает биографию актера, если она доступна, в противном случае 'Нет биографии для данного актера'.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            str: Биография актера или 'Нет биографии для данного актера'.
        """
        biography = actor_instance.biography
        if biography:
            return biography
        else:
            return 'No biography for current actor'

    def get_birth_place(self, actor_instance):
        """
        Возвращает место рождения актера, если оно доступно, в противном случае 'Неизвестно'.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            str: Место рождения актера или 'Неизвестно'.
        """
        birth_place = actor_instance.birth_place
        if birth_place:
            return birth_place
        else:
            return 'Unknown'

    def get_image(self, actor_instance):
        """
        Возвращает URL изображения актера, если оно доступно, в противном случае None.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            str или None: URL изображения актера или None.
        """
        image = actor_instance.image
        if image:
            if 'None' in image.url:
                return None
            else:
                return image
        else:
            return None

    def get_gender(self, actor_instance):
        """
        Возвращает пол актера, если он доступен, в противном случае 'Неизвестно'.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            str: Пол актера или 'Неизвестно'.
        """
        gender = actor_instance.gender
        if gender:
            for gender_choice in Gender.choices:
                if gender == gender_choice[0]:
                    gender = gender_choice[1]
            return gender
        else:
            return 'Unknown'

    def get_actor_movies(self, actor_instance):
        """
        Возвращает фильмы, в которых снималсят это актер.

        Аргументы:
            actor_instance (Actor): Экземпляр класса Actor.

        Возвращает:
            QuerySet: QuerySet фильмов, в которых снималсят это актер.
        """
        return actor_instance.actor_movies.all()

    def get_context_data(self, **kwargs):
        """
        Переопределяет базовый метод, чтобы добавить дополнительные данные контекста для отображения шаблона.

        Аргументы:
            **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Словарь с данными контекста.
        """
        context = super().get_context_data(**kwargs)
        actor = self.get_object()
        context['name'] = actor.name
        context['popularity'] = self.get_popularity(actor_instance=actor)
        context['image'] = self.get_image(actor_instance=actor)
        context['biography'] = self.get_biography(actor_instance=actor)
        context['birth_place'] = self.get_birth_place(actor_instance=actor)
        context['birth_date'] = self.get_birth_date(actor_instance=actor)
        context['actor_movies'] = self.get_actor_movies(actor_instance=actor)
        context['gender'] = self.get_gender(actor_instance=actor)
        return context
