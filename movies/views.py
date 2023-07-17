from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Movie
from actors.models import Actor
from django.views.generic import (
    DetailView,
    ListView,

)
from django.contrib import messages
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from icecream import ic
from django.db import transaction
from django.http import Http404
# Create your views here.


def mins_convert_hours(mins):
    """
    Конвертирует минуты в формат "часы минуты".

    Параметры:
        - mins (int): Количество минут.

    Возвращает:
        - str (str): Строковое представление времени в формате "часы минуты".
    """
    if mins < 60:
        return f'{mins}min'
    else:
        hours = mins // 60
        mins = mins % 60
        return f'{hours}h {mins}min'


class ShowMoviePageDetailView(DetailView):
    """
    Класс для отображения страницы детальной информации о фильме.

    Атрибуты:
        context_object_name (str): Имя переменной для объекта фильма в шаблоне.
        model (django.db.models.Model): Класс модели, представляющий фильма.
        template_name (str): Имя шаблона, используемого для отображения страницы с подробной информацией о фильме.
    """
    context_object_name = 'movie'
    model = Movie
    template_name = 'movies/movie_detail.html'

    def get_title(self, movie_instance):
        """
        Возвращает заголовок фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - str (str): Заголовок фильма.
            - None: Если заголовок слишком длинный.
        """
        if len((movie_instance.title)) <= 36:
            return movie_instance.title
        else:
            return None

    def get_runtime(self, movie_instance):
        """
        Возвращает продолжительность фильма в формате "часы минуты".

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - str (str): Продолжительность фильма в формате "часы минуты".
            - 'Unknown Runtime' (str): Если продолжительность неизвестна.
        """
        runtime = movie_instance.runtime
        if runtime:
            return mins_convert_hours(runtime)
        else:
            return 'Unknown Runtime'

    def get_orig_lang(self, movie_instance):
        """
        Возвращает оригинальный язык фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - str (str): Оригинальный язык фильма.
            - 'Unknown' (str): Если язык неизвестен.
        """
        original_language = movie_instance.original_language
        if original_language:
            return original_language
        else:
            return 'Unknown'

    def get_budjet(self, movie_instance):
        """
        Возвращает бюджет фильма в формате "бюджет USD".

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - str (str): Бюджет фильма в формате "сумма USD".
            - 'Unknown' (str): Если бюджет неизвестен.
        """
        budjet = movie_instance.budjet
        if budjet:
            return f'{budjet} USD'
        else:
            return 'Unknown'

    def get_overview(self, movie_instance):
        """
        Возвращает описание фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - str (str): Описание фильма.
            - 'No Description for current movie' (str): Если описание отсутствует.
        """
        overview = movie_instance.overview
        if overview:
            return overview
        else:
            return 'No Description for current movie'

    def get_popularity(self, movie_instance):
        """
        Возвращает популярность фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - float (float): Популярность фильма.
            - 'Unknown' (str): Если популярность неизвестна.
        """
        popularity = movie_instance.popularity
        if popularity:
            return popularity
        else:
            return 'Unknown'

    def get_vote_average(self, movie_instance):
        """
        Возвращает среднюю оценку фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - float (float): Средняя оценка фильма.
            - 'Unknown' (str): Если оценка неизвестна.
        """
        vote_average = movie_instance.vote_average
        if vote_average:
            return vote_average
        else:
            return 'Unknown'

    def get_vote_count(self, movie_instance):
        """
        Возвращает количество голосов для фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - int (int): Количество голосов для фильма.
            - None: Если количество голосов неизвестно.
        """
        vote_count = movie_instance.vote_count
        if vote_count:
            return vote_count
        else:
            return None

    def get_image(self, movie_instance):
        """
        Возвращает изображение фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - ImageField (ImageField): Изображение фильма.
            - None: Если изображение отсутствует.
        """
        image = movie_instance.image
        if image:
            if 'None' in image.url:
                return None
            else:
                return image
        else:
            return None

    def get_genres(self, movie_instance):
        """
        Возвращает жанры фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - QuerySet (QuerySet): QuerySet жанров фильма.
            - None: Если жанры неизвестны.
        """
        genres = movie_instance.genres
        if genres:
            return genres.all()
        else:
            return None

    def get_actors(self, movie_instance):
        """
        Возвращает актеров фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - QuerySet (QuerySet): QuerySet актеров фильма (максимум 4 актера).
            - None: Если актеры неизвестны.
        """
        actors = movie_instance.actors
        if actors:
            return actors.all()[:4]
        else:
            return None

    def get_release_date(self, movie_instance):
        """
        Возвращает дату релиза фильма.

        Параметры:
            - movie_instance (Movie): Объект фильма.

        Возвращает:
            - date (date): Дата релиза фильма.
            - None: Если дата релиза неизвестна.
        """
        release_date = movie_instance.release_date
        if release_date:
            return release_date
        else:
            return None

    def user_rate(self, request):
        """
        Проверяет, оценил ли пользователь фильм.

        Параметры:
            - request: Запрос пользователя.
        Возвращает:
            - rating (int/float): Оценка пользователя для фильма.
            - False: Если пользователь не аутентифицирован.
        """
        if request.user.is_authenticated:
            movie = self.get_object()
            user_profile = request.user.user_profile
            movie_ratings = user_profile.movie_ratings
            rating = movie_ratings.get(str(movie.tmbd_id))
            if rating:
                return rating
            return False
        return False
    
    def user_like(self, request):
        if request.user.is_authenticated:
            movie = self.get_object()
            user_profile = request.user.user_profile
            liked_movies = user_profile.liked_movies.all()
            if movie in liked_movies:
                return True
            return False
        return False

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста страницы детальной информации о фильме.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - context (dict): Словарь данных контекста.
        """
        context = super(ShowMoviePageDetailView,
                        self).get_context_data(**kwargs)
        movie_instance = self.get_object()
        context['full_title'] = movie_instance.title
        context['title'] = self.get_title(movie_instance=movie_instance)

        context['runtime'] = self.get_runtime(movie_instance=movie_instance)
        context['original_language'] = self.get_orig_lang(
            movie_instance=movie_instance)
        context['budjet'] = self.get_budjet(movie_instance=movie_instance)
        context['overview'] = self.get_overview(movie_instance=movie_instance)
        context['popularity'] = self.get_popularity(
            movie_instance=movie_instance)
        context['vote_average'] = self.get_vote_average(
            movie_instance=movie_instance)
        context['vote_count'] = self.get_vote_count(
            movie_instance=movie_instance)
        context['image'] = self.get_image(movie_instance=movie_instance)
        context['genres'] = self.get_genres(movie_instance=movie_instance)
        context['actors'] = self.get_actors(movie_instance=movie_instance)
        context['release_date'] = self.get_release_date(
            movie_instance=movie_instance)
        context['user_rate'] = self.user_rate(request=self.request)
        context['user_like'] = self.user_like(request=self.request)
        return context

    def get(self, request, *args, **kwargs):
        """
    Обрабатывает GET-запрос на страницу.
    Добавляет в сессию предыдущий url 

    Параметры:
        - request: Запрос пользователя.
        - *args: Дополнительные позиционные аргументы.
        - **kwargs: Дополнительные именованные аргументы.

    Возвращает:
        - HttpResponse: Ответ с содержимым страницы.
    """
        request.session['previous_url'] = request.build_absolute_uri()
        return super().get(request, *args, **kwargs)


class MovieActorsListView(ListView):
    """
    Класс для отображения списка актеров фильма.
    Атрибуты
        template_name (str): Имя шаблона для отображения.
        paginate_by (int): Количество актеров на странице.
        model (django.db.models.Model): Класс модели, представляющий аткера.
    """
    model = Actor
    template_name = 'movies/movie_actors.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста страницы со списком актеров фильма.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - context (dict): Словарь данных контекста.
        """
        context = super().get_context_data(**kwargs)
        movie_pk = self.kwargs.get('pk')
        current_movie = get_object_or_404(Movie, pk=movie_pk)
        context['current_movie'] = current_movie

        return context

    def get_queryset(self, **kwargs):
        """
        Получает QuerySet объектов актеров фильма.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - queryset (QuerySet): QuerySet объектов актеров фильма.
        """
        queryset = super().get_queryset()
        movie_pk = self.kwargs.get('pk')
        current_movie = get_object_or_404(Movie, pk=movie_pk)
        queryset = current_movie.actors.order_by('-popularity')[:18]
        return queryset


class ShowLatestMoviesListView(ListView):
    """
    Класс для отображения списка последних фильмов .
    Атрибуты
        template_name (str): Имя шаблона для отображения.
        paginate_by (int): Количество фильмов на странице.
        model (django.db.models.Model): Класс модели, представляющий фильма.
    """
    model = Movie
    template_name = 'movies/movies.html'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        """
        Получает QuerySet объектов последних вышедших фильмов.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - queryset (QuerySet): QuerySet объектов последних вышедших фильмов.
        """
        queryset = super().get_queryset()
        today = date.today()
        week_ago_date = today - timedelta(weeks=1)
        query = Q(release_date__gte=week_ago_date) & Q(release_date__lte=today)
        queryset = Movie.objects.filter(query).order_by('-popularity')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста страницы со списком последних вышедших фильмов.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - context (dict): Словарь данных контекста.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Latest Movies'
        return context


class ShowUpcomingMoviesListView(ListView):
    """
    Класс для отображения списка предстояющих фильмов .
    Атрибуты
        template_name (str): Имя шаблона для отображения.
        paginate_by (int): Количество фильмов на странице.
        model (django.db.models.Model): Класс модели, представляющий фильма.
    """
    model = Movie
    template_name = 'movies/movies.html'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        """
        Получает QuerySet объектов предстоящих фильмов.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - queryset (QuerySet): QuerySet объектов предстоящих фильмов.
        """
        queryset = super().get_queryset()
        today = date.today()
        query = Q(release_date__gt=today)
        queryset = Movie.objects.filter(query).order_by('-popularity')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста страницы со списком предстоящих фильмов.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - context (dict): Словарь данных контекста.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Upcoming Movies'
        return context


class ShowMonthTopMoviesListView(ListView):
    """
    Класс для отображения списка самых популярных фильмов за последний месяц.
    Атрибуты
        template_name (str): Имя шаблона для отображения.
        paginate_by (int): Количество фильмов на странице.
        model (django.db.models.Model): Класс модели, представляющий фильма.
    """
    model = Movie
    template_name = 'movies/movies.html'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        """
        Получает QuerySet объектов самых популярных фильмов за последний месяц.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - queryset (QuerySet): QuerySet объектов самых популярных фильмов за последний месяц.
        """
        queryset = super().get_queryset()
        today = date.today()
        month_ago_date = today - timedelta(days=30)
        query = Q(release_date__lte=today) & Q(
            vote_average__gte=3) & Q(release_date__gte=month_ago_date)
        queryset = Movie.objects.filter(query).order_by('-popularity')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста страницы со списком самых популярных фильмов за последний месяц.

        Параметры:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            - context (dict): Словарь данных контекста.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Top Month Movies'
        return context


class UserRateMovieDetailView(LoginRequiredMixin, DetailView):
    """
    Класс для отображения оценки фильма пользователем.

        Атрибуты:
            model (django.db.models.Model): Класс модели, представляющий фильма.
    """
    model = Movie

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос на оценку фильма пользователем.

        Параметры:
            - request: Запрос пользователя.
            - *args: Дополнительные позиционные аргументы.
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            - HttpResponse: Ответ с перенаправлением на страницу детальной информации о фильме.
        """
        movie = self.get_object()
        tmbd_id = movie.tmbd_id
        user_profile = request.user.user_profile

        rate_sum = movie.vote_count * movie.vote_average
        rate_value = request.POST.get('rate_value')
        try:
            rate_value = int(rate_value)
        except ValueError:
            messages.error(request, 'Invalid Rate: Enter Valid Number')
            return redirect('movies:movie_detail', pk=movie.pk)
        new_vote_count = movie.vote_count + 1
        new_vote_average = (rate_sum + rate_value) / new_vote_count
        new_movie_ratings = user_profile.movie_ratings
        new_movie_ratings.setdefault(str(tmbd_id), rate_value)
        with transaction.atomic():
            user_profile.movie_ratings = new_movie_ratings
            user_profile.save()
            movie.vote_count = new_vote_count
            movie.vote_average = new_vote_average
            movie.save()

        return redirect('movies:movie_detail', pk=movie.pk)


class UserDeleteRateMovieDetailView(LoginRequiredMixin, DetailView):
    """
    Класс для отображения удаления оценки фильма пользователем.

        Атрибуты:
            model (django.db.models.Model): Класс модели, представляющий фильма.
    """
    model = Movie

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на удаление оценки фильма пользователем.

        Параметры:
            - request: Запрос пользователя.
            - *args: Дополнительные позиционные аргументы.
            - **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            - HttpResponse: Ответ с перенаправлением на страницу детальной информации о фильме.
        """
        movie = self.get_object()
        tmbd_id = movie.tmbd_id
        user_profile = request.user.user_profile

        rate_sum = movie.vote_count * movie.vote_average
        movie_ratings = user_profile.movie_ratings
        rate_value = movie_ratings.get(str(movie.tmbd_id))
        new_vote_count = movie.vote_count - 1
        new_vote_average = (rate_sum - rate_value) / new_vote_count
        new_movie_ratings = user_profile.movie_ratings
        new_movie_ratings.pop(str(tmbd_id))
        with transaction.atomic():
            user_profile.movie_ratings = new_movie_ratings
            user_profile.save()
            movie.vote_count = new_vote_count
            movie.vote_average = new_vote_average
            movie.save()

        return redirect('movies:movie_detail', pk=movie.pk)

class UserLikeUnlikeMovie(LoginRequiredMixin, DetailView):
    model = Movie
    def get(self, request, *args, **kwargs):
        movie = self.get_object()
        user_profile = request.user.user_profile
        action = kwargs.get('action')
        if action == 'like':
            if movie not in user_profile.liked_movies.all():
                with transaction.atomic():
                    movie.likes_count += 1
                    movie.save()
                    user_profile.liked_movies.add(movie)
                    user_profile.save()
                return redirect('movies:movie_detail',pk = movie.pk )
            else:
                messages.warning(request,'You can not like movie more than one time')
                return redirect('movies:movie_detail',pk = movie.pk )
        elif action == 'unlike':
            if movie  in user_profile.liked_movies.all():
                with transaction.atomic():
                    movie.likes_count -= 1
                    movie.save()
                    user_profile.liked_movies.remove(movie)
                    user_profile.save()
                return redirect('movies:movie_detail',pk = movie.pk )
            else:
                messages.warning(request,'You can not unlike movie more than one time')
                return redirect('movies:movie_detail',pk = movie.pk )
        else:
            raise Http404('Page not fount')



