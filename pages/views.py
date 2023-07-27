from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
)
from movies.models import Movie, Keyword
from articles.models import Article, Comment
from datetime import date, timedelta
from icecream import ic
from pathlib import Path
import os
from django.conf import settings
from users.forms import UserForm, UserProfileForm
from users.models import User, UserProfile
from django.contrib import messages
# Create your views here.


def delete_avatar(url):
    url = os.path.basename(url)
    file_path = Path(settings.MEDIA_AVATARS_ROOT, url)
    os.remove(file_path)


class MainpageTemplateView(TemplateView):
    """
    Класс представления главной страницы.

    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - get_latest_movies() -> QuerySet[Movie]: Возвращает последние фильмы, выпущенные за последнюю неделю.
        - get_upcoming_movies() -> QuerySet[Movie]: Возвращает предстоящие фильмы.
        - get_popular_month_movies() -> QuerySet[Movie]: Возвращает популярные фильмы последнего месяца.
        - get_latest_articles() -> QuerySet[Article]: Возвращает последние статьи.
        - get_context_data(**kwargs) -> dict: Возвращает контекст данных для передачи в шаблон.

    """
    template_name = 'pages/mainpage/index.html'

    def get_latest_movies(self):
        """
        Возвращает последние фильмы, выпущенные за последнюю неделю.

        Возвращает:
            QuerySet[Movie]: Последние фильмы.

        """
        today = date.today()
        week_ago_date = today - timedelta(weeks=1)
        query = Q(release_date__gte=week_ago_date) & Q(release_date__lte=today)
        # exclude_query = Q(image = 'None')
        latest_movies = Movie.objects.filter(query).order_by('-vote_count')[:8]
        return latest_movies

    def get_upcoming_movies(self):
        """
        Возвращает предстоящие фильмы.

        Возвращает:
            QuerySet[Movie]: Предстоящие фильмы.
        """
        today = date.today()
        month_after_date = today + timedelta(days=30)
        query = Q(release_date__gt=today) & Q(
            release_date__lte=month_after_date)
        upcoming_movies = Movie.objects.filter(query)[:3]

        return upcoming_movies

    def get_popular_month_movies(self):
        """
        Возвращает популярные фильмы последнего месяца.

        Возвращает:
            QuerySet[Movie]: Популярные фильмы.
        """
        today = date.today()
        month_ago_date = today - timedelta(days=30)
        query = Q(release_date__lte=today) & Q(
            release_date__gte=month_ago_date)
        month_popular_movies = Movie.objects.filter(
            query).order_by('-popularity')[:8]
        return month_popular_movies

    def get_latest_articles(self):
        """
        Возвращает последние 3 статьи которые одобрены

        Возвращает:
            QuerySet[Article]: Последние статьи.
        """
        articles = Article.objects.filter(
            approved=True).order_by('-updated_at')[:3]
        return articles

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст данных для передачи в шаблон.

        Аргументы:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Контекст данных.
        """
        context = super().get_context_data(**kwargs)
        context['latest_movies'] = self.get_latest_movies()
        context['upcoming_movies'] = self.get_upcoming_movies()
        context['popular_movies'] = self.get_popular_month_movies()
        context['latest_articles'] = self.get_latest_articles()
        access = self.request.COOKIES.get('access_token')
        return context


class FilteredMoviesListView(ListView):
    """
    Класс представления списка отфильтрованных фильмов.

    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.
        - paginate_by (int): Количество элементов на странице при пагинации.

    Методы:
        - set_filter_title(option: int) -> str: Возвращает заголовок фильтра на основе выбранного варианта.
        - get_queryset() -> QuerySet[Movie]: Возвращает набор данных фильмов в зависимости от выбранного фильтра.
        - get_context_data(**kwargs) -> dict: Возвращает контекст данных для передачи в шаблон.

    """
    template_name = 'pages/movies/filter_movies.html'
    paginate_by = 6

    def set_filter_title(self, option):
        """
        Возвращает заголовок фильтра на основе выбранного варианта.

        Аргументы:
            - option (int): Выбранный вариант фильтра.

        Возвращает:
            str: Заголовок фильтра.
        """
        if option == 0:
            return 'Set Filter To Search For Movies'
        elif option == 1:
            return 'This Year Movies'
        elif option == 2:
            return 'The Most Popular Movies'
        elif option == 3:
            return 'Top Rated Movies'
        elif option == 4:
            return 'The Oldest Movies'
        else:
            return 'Set Right Filter To Search For Movies'

    def get_queryset(self):
        """
        Возвращает набор данных фильмов в зависимости от выбранного фильтра.

        Возвращает:
            QuerySet[Movie]: Набор данных фильмов.

        """
        queryset = Movie.objects.none()
        option = self.kwargs.get('option')
        if option:
            if option == 1:
                today = date.today()
                this_year = today.year
                this_year_first_day = date(this_year, 1, 1)
                filter_q = Q(release_date__gte=this_year_first_day)
                queryset = Movie.objects.filter(
                    filter_q).order_by('-popularity')
            elif option == 2:
                queryset = Movie.objects.order_by('-popularity')[:150]
            elif option == 3:
                queryset = Movie.objects.filter(
                    vote_average__gte=8).order_by('-vote_count')[:150]
            elif option == 4:
                start_date = date(1900, 1, 1)
                end_date = date(1990, 1, 1)
                filter_q = Q(release_date__gte=start_date) & Q(
                    release_date__lte=end_date)
                queryset = Movie.objects.filter(
                    filter_q).order_by('release_date')[:150]
            queryset = queryset.prefetch_related('genres')

        else:
            queryset = Movie.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст данных для передачи в шаблон.

        Аргументы:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Контекст данных.
        """
        context = super().get_context_data(**kwargs)
        context['filter_title'] = self.set_filter_title(
            option=self.kwargs.get('option'))
        return context


def filter_movies(request):
    """
    Функция-обработчик фильтрации фильмов.
    Получает вариант филбтрации и отправляет вариант на обработку в FilteredMoviesListView


    Аргументы:
        - request (HttpRequest): Запрос клиента.

    Возвращает:
        HttpResponse: Перенаправление в FilteredMoviesListView
    """
    if request.method == 'POST':
        option = request.POST.get("filter_choice")
        option = int(option)
        return redirect('pages:filtered_movies', option=option)
    else:
        return redirect('pages:filtered_movies', option=0)


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    """
    Класс представления профиля пользователя.

    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - user_has_avatar(user: User) -> Optional[ImageFieldFile]: Проверяет наличие аватара у пользователя.
        - get_context_data(**kwargs) -> dict: Возвращает контекст данных для передачи в шаблон.
        - post(request: HttpRequest, *args, **kwargs) -> HttpResponse: Обрабатывает POST-запрос на обновление профиля.
    """
    template_name = 'pages/profile.html'

    def user_has_avatar(self, user):
        """
        Проверяет наличие аватара у пользователя.

        Аргументы:
            - user (User): Пользователь.

        Возвращает:
            Optional[ImageFieldFile]: Аватар пользователя или None, если аватар отсутствует
        """
        avatar = user.user_profile.avatar
        if avatar:
            return avatar
        else:
            return None

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст данных для передачи в шаблон.

        Аргументы:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Контекст данных.
        """
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        context['user_profile_form'] = UserProfileForm(
            instance=self.request.user.user_profile)
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос на обновление профиля.

        Аргументы:
            - request (HttpRequest): Запрос клиента.
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.

        Возвращает:
            HttpResponse: HTTP-ответ.
        """
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_profile_form.save()
            user_form.save()
        

            messages.success(request, 'Your profile is updated successfully')
            return redirect('pages:profile_page')
        else:
            errors = user_form.errors.as_data()
            for error in errors:
                messages.error(
                    request, f'{error} - {errors[error][0].message}')
            errors = user_profile_form.errors.as_data()
            for error in errors:
                messages.error(
                    request, f'{error} - {errors[error][0].message}')

            user_form = UserForm(instance=request.user)
            user_profile_form = UserProfileForm(
                instance=request.user.user_profile)
            context = self.get_context_data(kwargs=kwargs)
            context['user_form'] = user_form
            context['user_profile_form'] = user_profile_form

            return render(request, self.template_name, context=context)


class SearchResultsListView(ListView):
    """
    Класс представления страницы с результатами поиска.

    Атрибуты:
        - paginate_by (int): Количество элементов на странице при пагинации.
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - get_movies_by_keywords(query: str) -> List[Movie]: Возвращает фильмы, связанные с ключевыми словами запроса.
        - get_context_data(**kwargs) -> dict: Возвращает контекст данных для передачи в шаблон.
        - get_queryset() -> Union[List[Movie], QuerySet[Movie]]: Возвращает набор данных фильмов в зависимости от запроса.

    """
    paginate_by = 6
    template_name = 'pages/search/search_results.html'

    def get_movies_by_keywords(self, query):
        """
        Возвращает фильмы, если запрос связан с ключевыми словами фильмов.

        Аргументы:
            - query (str): Запрос пользователя.

        Возвращает:
            List[Movie]: Фильмы, связанные с ключевыми словами запроса.
        """
        movies = []
        query_parts = query.split(' ')
        for query_part in query_parts:
            if query_part:
                keywords = Keyword.objects.filter(name__icontains=query_part)
                if keywords:
                    for keyword in keywords:
                        for movie in keyword.keyword_movies.all():
                            movies.append(movie)
        return movies

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст данных для передачи в шаблон.

        Аргументы:
            - **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Контекст данных.
        """
        context = super().get_context_data(**kwargs)
        query = self.kwargs.get('query')
        if query:
            context['query'] = query
        return context

    def get_queryset(self):
        """
        Возвращает набор данных фильмов в зависимости от запроса.

        Возвращает:
            Union[List[Movie], QuerySet[Movie]]: Набор данных фильмов.
        """
        query = self.kwargs.get('query')
        if query:

            movies1 = list(Movie.objects.filter(title__icontains=query))
            movies2 = self.get_movies_by_keywords(query=query)
            movies_wthout_repeat = set(movies2)
            movies1.extend(movies_wthout_repeat)
            if movies1:
                no_duplicate_movies = []
                for movie in movies1:
                    if movie not in no_duplicate_movies:
                        no_duplicate_movies.append(movie)

                return no_duplicate_movies
            else:
                return Movie.objects.none()
        else:
            return Movie.objects.none()


def search_movies(request):
    """
    Функция-обработчик поиска фильмов.
    Получив запрос отправляет его в SearchResultsListView

    Аргументы:
        - request (HttpRequest): Запрос клиента.

    Возвращает:
        HttpResponse: Перенаправление в SearchResultsListView.
    """
    if request.method == 'POST':
        query = request.POST.get('search-input')
        query = query.strip()
        if query:
            return redirect('pages:search_results', query=query)
        return redirect('pages:search_results', query='#####')
    else:
        return redirect('pages:search_results', query='#####')


class UserArticlesListView(UserPassesTestMixin, ListView):
    """
    Класс представления списка статей автора.

    Атрибуты:
        - permission_required (List[str]): Разрешения, необходимые для доступа к странице.
        - paginate_by (int): Количество элементов на странице при пагинации.
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - test_func() -> bool: Проверяет разрешение пользователя на доступ к странице.
        - get_queryset() -> QuerySet[Article]: Возвращает набор данных статей пользователя.
    """

    def test_func(self):
        """
        Проверяет разрешение пользователя на доступ к странице.

        Возвращает:
            bool: True, если пользователь в персонале, False в противном случае.
        """
        return self.request.user.is_staff
    permission_required = ['articles.add_article']
    paginate_by = 3
    template_name = 'pages/articles/user_articles.html'

    def get_queryset(self):
        """
        Возвращает набор  статей пользователя.

        Возвращает:
            QuerySet[Article]: Набор  статей пользователя.
        """
        user = self.request.user
        user_articles = user.author_articles.all().order_by('-updated_at')
        return user_articles


class UserFavoriteMoviesListView(LoginRequiredMixin, ListView):
    """
    Класс представления списка любимых фильмов пользователя.

    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.
        - paginate_by (int): Количество элементов на странице при пагинации.

    Методы:
        - get_queryset() -> QuerySet[Movie]: Возвращает набор данных избранных фильмов пользователя.
        - get() -> HttpResponse: Обрабатывает GET-запрос на получение страницы.
    """
    template_name = 'pages/favorite_movies.html'
    paginate_by = 4

    def get_queryset(self):
        """
        Возвращает набор данных любимых фильмов пользователя.

        Возвращает:
            QuerySet[Movie]: Набор данных любимых фильмов пользователя.
        """
        user_profile = self.request.user.user_profile
        favorite_movies = user_profile.favorite_movies.all()

        return favorite_movies

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на получение страницы.
        Ложит в сессию значения своего url

        Аргументы:
            - request (HttpRequest): Запрос клиента.
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.

        Возвращает:
            HttpResponse: HTTP-ответ.
        """
        request.session['previous_url'] = request.build_absolute_uri()
        return super().get(request, *args, **kwargs)


class UserFavoriteMoviesAddDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления добавления фильма в любимое пользователя.

    Атрибуты:
        - model (Model): Класс модели фильма.

    Методы:
        - get() -> HttpResponse: Обрабатывает GET-запрос на добавление фильма в любимое пользователя.

    """
    model = Movie

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на добавление фильма в избранное пользователя.
        Если фильм уже в любимых то ничего не делается
        Аргументы:
            - request (HttpRequest): Запрос клиента.
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.

        Возвращает:
            HttpResponse: HTTP-ответ.
        """
        previous_url = request.session.get('previous_url')
        user_profile = request.user.user_profile
        movie = self.get_object()
        if movie not in user_profile.favorite_movies.all():
            user_profile.favorite_movies.add(movie)
        if not previous_url:
            return redirect('movies:movie_detail', pk=kwargs.get('pk'))
        return redirect(previous_url)


class UserFavoriteMoviesRemoveDetailView(LoginRequiredMixin, DetailView):
    """
    Класс представления удаления фильма из любимого пользователя.

    Атрибуты:
        - model (Model): Класс модели фильма.

    Методы:
        - get() -> HttpResponse: Обрабатывает GET-запрос на удаление фильма из любимого пользователя.

    """
    model = Movie

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на удаление фильма из любимого для пользователя.
        Если фильм уже в не  любимых то ничего не делается
        Аргументы:
            - request (HttpRequest): Запрос клиента.
            - *args: Позиционные аргументы.
            - **kwargs: Именованные аргументы.

        Возвращает:
            HttpResponse: HTTP-ответ.
        """
        previous_url = request.session.get('previous_url')

        user_profile = request.user.user_profile
        movie = self.get_object()
        if movie in user_profile.favorite_movies.all():
            user_profile.favorite_movies.remove(movie)
        if not previous_url:
            return redirect('movies:movie_detail', pk=kwargs.get('pk'))
        return redirect(previous_url)

class ModeratorCommentsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 8
    template_name = 'pages/moderator/comments.html'
    
    def test_func(self):
        user = self.request.user
        if user.is_moderator:
            return True
        return False

    def get_queryset(self):
        comments = Comment.objects.select_related('author','article')
        return comments

    def get(self, request, *args, **kwargs):
        request.session['previous_url'] = request.build_absolute_uri()
        return super().get(request, *args, **kwargs)