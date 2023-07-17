from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView
)

from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin
)
from .models import Article, Comment
from .forms import (
    ArticleForm,
    CommentForm
)
from icecream import ic
from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
# Create your views here.


class ShowArticlesListView(ListView):
    """
    Контроллер класса  для отображения списка статей.

    Атрибуты класса:
        template_name (str): Имя шаблона для отображения.
        paginate_by (int): Количество статей на странице.

    Методы:
        get_queryset(): Возвращает список статей
        get_user_articles(user): Возвращает статьи, доступные пользователю для редактирования и удаления
        get_context_data(**kwargs): Метод чтобы добавить  данные контекста для отображения шаблона.

    """
    template_name = 'articles/articles_list.html'
    paginate_by = 3

    def get_queryset(self):
        """
        Возвращает список статей которые одобрены, сортировка идет по времени обновления

        Возвращаемое значение:
            QuerySet: Список статей

        """
        qs = Article.objects.filter(approved=True).order_by('-updated_at')
        return qs

    def get_user_articles(self, user):
        """
        Возвращает статьи, доступные пользователю для редактирования и удаления

        Возвращаемое значение:
            QuerySet: Список статей

        """
        user_articles = get_objects_for_user(user, 'articles.change_article')
        return user_articles

    def get_context_data(self, **kwargs):
        """
        Переопределяет базовый метод, чтобы добавить дополнительные данные контекста для отображения шаблона.


        Аргументы:
            **kwargs: Дополнительные аргументы.

        Возвращает:
            dict: Словарь с данными контекста.
        """
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = self.get_queryset()[:3]
        context['user_articles'] = self.get_user_articles(
            user=self.request.user)
        return context


class ShowArticleDetailView(DetailView):
    """
    Контроллер класса  для отображения одной статьи

    Атрибуты класса:
        template_name (str): Имя шаблона для отображения.
        context_object_name (str): Имя переменной для объекта статьи в шаблоне.
        model (django.db.models.Model): Класс модели, представляющий статью.

    Методы:
        is_user_author_article(): Возвращает идентификатор есть ли у пользователся право изменять
        эту стаью
        get_user_articles(user): Возвращает статьи, доступные пользователю для редактирования и удаления
        get_context_data(**kwargs): Метод чтобы добавить  данные контекста для отображения шаблона.
        get() : Базовый метод который работает при get запросе
        post() : Базовый метод который работает при post запросе

    """
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    model = Article

    def is_user_author_article(self, user):
        """
        Проверяет, является ли пользователь автором статьи.

        Args:
            user (User): Пользователь, для которого проверяется авторство.

        Возвращает:
            bool: True, если пользователь является автором статьи. Иначе False.
        """
        return user.has_perm('articles.change_article', self.get_object())
    def get_comments_wthout_parent_comment(self):
        comments = Comment.objects.filter(
            article=self.get_object()).order_by('-created_at').select_related('article','author')
        without_parent_comments = []
        for comment in comments:
            if not comment.parent_comment:
                without_parent_comments.append(comment)
        return without_parent_comments
    def get_context_data(self, **kwargs):
        """
        Получает контекст данных для отображения шаблона.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_comments_wthout_parent_comment()
        context['latest_articles'] = Article.objects.filter(
            approved=True).order_by('-updated_at')[:3]
        context['is_user_author_article'] = self.is_user_author_article(
            user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос.
        Если статья одобрена то будет статься показана
        В противном случае:
            Если юзер это автор стаьи то будет статья показана
            Если нет, то бдует возбуждена PermissionDenied

        Args:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ на запрос.

        Raises:
            PermissionDenied: Вызывается, если пользователь не имеет доступа к статье.
        """
        movie = self.get_object()
        user = self.request.user
        if movie.approved:
            return super().get(request, *args, **kwargs)
        if self.is_user_author_article(user=user):
            return super().get(request, *args, **kwargs)
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос. Создание комментария
        Проверяет аутентификацию юзера чтобы создать комент, в противном случае
        он переотправляется залогиниться

        Args:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные аргументы.

        Возвращает:
            Если юзер залогинин то вызывается get()
            В противном случае перенаправляется в страницу логина
        """
        if request.user.is_authenticated:
            new_comment = Comment.objects.create(
                text=request.POST.get("comment"),
                author=request.user,
                article=self.get_object(),
            )
            new_comment.save()
            return self.get(request, *args, **kwargs)
        else:
            next_url = reverse('registration:login') + '?next=' + reverse(
                'articles:article_detail', kwargs={'slug': self.get_object().slug})

            return redirect(next_url)


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Контроллер класса  для удаления статьи

    Атрибуты класса:
        template_name (str): Имя шаблона для отображения.
        context_object_name (str): Имя переменной для объекта статьи в шаблоне.
        model (django.db.models.Model): Класс модели, представляющий статью.
        permission_required(Permission): Разрешение для отображения данного вью
        raise_exception(bool): Если True возбуждает 403 ошибку, в противном случае отправляет на страницу логина
    Методы:
        form_valid(form): Функция вызывается если форма правильно заполнена

    """
    context_object_name = 'article'
    template_name = 'articles/article_delete.html'
    model = Article
    permission_required = 'articles.delete_article'
    raise_exception = True

    success_url = reverse_lazy('pages:user_articles')

    def form_valid(self, form):
        """
        Выполняет действия после успешного удаления статьи.

        Args:
            form (Form): Форма.

        Returns:
            HttpResponse: ответ от родительского класса
        """
        messages.success(self.request, "The Article was deleted successfully.")
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Контроллер класса  для обновления статьи

    Атрибуты класса:
        template_name (str): Имя шаблона для отображения.
        context_object_name (str): Имя переменной для объекта статьи в шаблоне.
        model (django.db.models.Model): Класс модели, представляющий статью.
        permission_required(Permission): Разрешение для отображения данного вью
        raise_exception(bool): Если True возбуждает 403 ошибку, в противном случае отправляет на страницу логина
    Методы:
        get_context_data(kwargs): Метод чтобы добавить  данные контекста для отображения шаблона.
        form_valid(form) : Функция вызывается если форма правильно заполнена
    """
    template_name = 'articles/article_form.html'
    model = Article
    permission_required = 'articles.change_article'
    raise_exception = True
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        """
        Получает контекст данных для отображения шаблона.
        action(str) - действие которое происходит
        artilce(Article)- экземпляр модели Article
        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст данных для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context['article'] = self.get_object()
        return context

    def form_valid(self, form):
        """
        Выполняет действия после успешного обновления статьи.

        Args:
            form (Form): Форма.

        Returns:
            HttpResponse: ответ от родительского класса
        """
        messages.success(self.request, 'Article was updated successfully')
        return super().form_valid(form)


class ArticleCreateView(UserPassesTestMixin, CreateView):
    """
    Контроллер класса  для создания статьи

    Атрибуты класса:
        template_name (str): Имя шаблона для отображения.
        model (django.db.models.Model): Класс модели, представляющий статью.
        form_class(Form) : Форма для создания статьи
    Методы:
        test_func(): Метод проверяющий может ли юзер смотреть этот вью
        get_context_data(kwargs): Метод чтобы добавить  данные контекста для отображения шаблона.
        form_valid(form) : Функция вызывается если форма правильно заполнена
    """

    form_class = ArticleForm
    model = Article
    template_name = 'articles/article_form.html'

    def test_func(self):
        """
        Метод проверяющий может ли юзер смотреть этот вью

        Возвращает:
            bool - True если пользовтель явлется персоналом, в противном случае False
        """
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        """
    Получает контекст данных для отображения шаблона.

    Этот метод переопределяет метод get_context_data() базового класса.
    Он добавляет значение 'action' в контекст, указывающее на действие 'create'.

    Аргументы:
        **kwargs: Дополнительные именованные аргументы.

    Возвращает:
        dict: Контекстные данные.
    """
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context

    def form_valid(self, form):
        """
    Обрабатывает проверку корректности данных формы и создает новую статью.

    Этот метод вызывается, когда данные формы являются корректными.
    Он извлекает очищенные данные из формы, создает новый объект статьи,
    сохраняет его в базе данных и выполняет перенаправление на страницу с подробностями статьи.

    Аргументы:
        form (Form): Проверенная форма.

    Возвращает:
        HttpResponseRedirect: Ответ перенаправления на страницу с подробностями статьи.
    """
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        image = form.cleaned_data['image']
        new_article = Article(author=self.request.user,
                              title=title,
                              content=content)
        if image:
            new_article.image = image

        new_article.save()
        messages.success(self.request, 'Article was created successfully')
        return redirect('articles:article_detail', slug=new_article.slug)


class ArticleCommentDeleteView(UserPassesTestMixin, DeleteView):
    """
    Представление для удаления комментария к статье.

    Это представление позволяет пользователям удалять собственные комментарии или комментарии, если они являются суперпользователем.
    Оно требует, чтобы пользователь прошел проверку, определенную в методе `test_func`.

    Атрибуты:
        context_object_name (str): Имя переменной, используемой в шаблоне для объекта комментария.
        template_name (str): Имя шаблона для отображения страницы удаления комментария.
        model (Model): Класс модели комментария.
        success_url (str): URL для перенаправления после успешного удаления комментария.

    Методы:
        test_func(): Проверяет, является ли пользователь суперпользователем или автором комментария.
        get_context_data(**kwargs): Добавляет объект статьи в контекстные данные.
        get_object(): Получает объект комментария на основе его уникального айди.
        form_valid(form): Удаляет комментарий и возвращает сообщение об успешном удалении.
        get_success_url(): Получает идентификатор статьи и выполняет перенаправление на страницу деталей статьи.
    """
    context_object_name = 'comment'
    template_name = 'comments/comment_delete.html'
    model = Comment
    success_url = reverse_lazy('pages:user_articles')

    def test_func(self):
        """
        Проверяет, является ли пользователь суперпользователем или автором комментария.

        Возвращает:
            bool: True, если пользователь является суперпользователем или автором комментария, иначе False.
        """
        user = self.request.user
        if user.is_superuser:
            return True
        comment = self.get_object()
        if comment in user.author_comments.all():
            return True
        return False

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для представления.

        Этот метод переопределяет метод get_context_data() базового класса.
        Он добавляет объект статьи в контекстные данные.

        Аргументы:
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            dict: Контекстные данные.
        """
        context = super().get_context_data(**kwargs)
        article_slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=article_slug)
        context['article'] = article
        return context

    def get_object(self):
        """
        Возвращает объект комментария на основе его идентификатора.

        Возвращает:
            Comment: Объект комментария.
        """
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, uuid=comment_id)
        return comment

    def form_valid(self, form):
        """
        Обрабатывает проверку корректности данных формы и удаляет комментарий.

        Этот метод вызывается, когда данные формы являются корректными.
        Он удаляет объект комментария из базы данных и возвращает сообщение об успешном удалении.

        Аргументы:
            form (Form): Проверенная форма.

        Возвращает:
            HttpResponseRedirect: Ответ перенаправления.
        """
        comment = self.get_object()
        comment.delete()
        messages.success(self.request, "The Comment was deleted successfully.")
        return self.get_success_url()

    def get_success_url(self):
        """
        Возвращает  URL для перенаправления.

        Возвращает:
            HttpResponseRedirect: Ответ перенаправления на страницу деталей статьи.
        """
        article_slug = self.kwargs.get('slug')
        get_object_or_404(Article, slug=article_slug)
        return redirect('articles:article_detail', slug=article_slug)

class ArticleAddChildCommentCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    template_name = 'comments/comment_add.html'
    model = Comment
    form_class = CommentForm
    def test_func(self):
        user = self.request.user
        comment = self.get_object()
        if user is not comment.author:
            return True
        return False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=article_slug)
        context['article'] = article
        ic(self.get_object())
        return context

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        parent_comment = get_object_or_404(Comment, uuid=comment_id)
        return parent_comment

    def form_valid(self, form):
        context = self.get_context_data()
        text = form.cleaned_data['text']
        article = context['article']
        parent_comment = self.get_object()
        comment = Comment(article = article, parent_comment = parent_comment,
                        text=text, author = self.request.user)
        comment.save()
        return self.get_success_url()
    def get_success_url(self):
        article_slug = self.kwargs.get('slug')
        get_object_or_404(Article, slug=article_slug)
        messages.success(self.request, 'Yout comment was successfully added')
        return redirect('articles:article_detail', slug=article_slug)
    