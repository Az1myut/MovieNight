from django.shortcuts import render, redirect
from django.urls import reverse_lazy, resolve, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerialzer
from .forms import LoginForm
from users.models import User
from django.views.generic.base import TemplateView, View
from icecream import ic
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
import jwt
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import OutstandingToken
# Create your views here.


class RegisterView(TemplateView):
    """
    Класс для отображения страницы регистрации пользователя.
    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - post(request: HttpRequest, *args, **kwargs) -> HttpResponse: Обрабатывает POST-запрос на регистрацию пользователя.
    """
    template_name = 'registration/register.html'

    def post(self, request):
        """
        Обрабатывает POST-запрос на регистрацию пользователя.
        Сначала идет реквест на RegisterApi если пользователь зарегистрировался то он
        будет перенаправлен на страницу логина, в противном случае будет отображена эта страница с ошибками

        Параметры:
            - request: Запрос пользователя.

        Возвращает:
            - HttpResponse: Ответ на запрос.
            если пользователь зарегистрировался то он
            будет перенаправлен на страницу логина, в противном случае будет отображена эта страница с ошибками
        """
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.add_message(request, messages.INFO,
                                 "Passwords don't match")
            return render(request, template_name=self.template_name)
        if password1 == '' or password2 == '' or email == '':
            messages.add_message(request, messages.WARNING, "Enter data")
            return render(request, template_name=self.template_name)
        response = requests.post('http://127.0.0.1:8000/registration/api/register/', data={'email': email,
                                                                                           'password': password1})
        if response.status_code == 200:

            messages.add_message(request, messages.SUCCESS,
                                 "You are successfully registered")

            return redirect('registration:login')

        else:

            errors = response.json()
            email_erros = errors.get('email')
            password_errors = errors.get('password')
            if email_erros is not None:
                for error in email_erros:
                    messages.add_message(request, messages.WARNING, f"{error}")
            if password_errors is not None:
                for error in password_errors:
                    messages.add_message(request, messages.WARNING, f"{error}")
            return render(request, template_name=self.template_name)


class LoginView(TemplateView):
    """
    Класс для отображения страницы аутентификации пользователя.
    Атрибуты:
        - template_name (str): Имя шаблона для отображения страницы.

    Методы:
        - post(request: HttpRequest, *args, **kwargs) -> HttpResponse: Обрабатывает POST-запрос на регистрацию пользователя.
        - get(request: HttpRequest, *args, **kwargs) -> HttpResponse: Обрабатывает GET-запрос
    """
    template_name = 'registration/login.html'
    form_class = LoginForm

    def post(self, request):
        """
        Обрабатывает POST-запрос на аутентификацию пользователя.
        Сначала идет реквест на TokenObtainPairView чтобы аутенфицировать  пользователя 
        Если он аутентифирован то он будет перенаправлен на next или mainpage также аксес токен будет сохранен в куки
        В противном случае удет отображена эта страница с ошибками

        Параметры:
            - request: Запрос пользователя.

        Возвращает:
            - HttpResponse: Ответ на запрос.
        """
        form = self.form_class(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            response = requests.post('http://127.0.0.1:8000/api/token/', data={'email': email,
                                                                               'password': password})
    
            if response.status_code == 200:
                authenticated_user = User.objects.get(email=email)
                login(request, authenticated_user,
                      backend=settings.AUTHENTICATION_BACKENDS[0])
                data = response.json()
                access_token = data['access']

                if request.POST.get('next'):
                    resolver_match = resolve(request.POST.get('next'))
                    kwargs = resolver_match.kwargs
                    new_kwargs = {}
                    if kwargs:
                        for key, value in kwargs.items():
                            new_kwargs[key] = value
                    redirect_value = resolver_match.view_name
                    resp = HttpResponseRedirect(
                        reverse(redirect_value, kwargs=new_kwargs))
                    
                else:
                    resp = HttpResponseRedirect(reverse_lazy('pages:mainpage'))

                resp.set_cookie('access_token', access_token)
                return resp

            else:
                result = response.json()
                result = dict(result)
                for key, value in result.items():
                    if key == 'detail':
                        messages.add_message(
                            request, messages.WARNING, f"{value}")
                    else:
                        for error in value:
                            messages.add_message(
                                request, messages.WARNING, f"{error}")
        else:
            errors = form.errors.as_data()
            for error in errors:
                messages.warning(
                    request, f'{error} - {errors[error][0].message}')

        return render(request=request, template_name=self.template_name)

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на аутентификацию пользователя.
        Если пользователь зарегистрирован то будет перенапрвлен на страницу главной страницы
        В противном отработает get запрос родительского класса

        Параметры:
            - request: Запрос пользователя.

        Возвращает:
            - HttpResponse: Ответ на запрос.
        """
        if request.user.is_authenticated:
            return redirect('pages:mainpage')
        return super().get(request, *args, **kwargs)


class LogoutView(View):
    """
    Класс для выхода пользователя из системы.

    Методы:
        get -  Обрабатывает GET-запрос на выход пользователя из системы.
    """

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос на выход пользователя из системы.
        Удаляет его рефреш токен из базы и также его акссесс токен из куки

        Параметры:
            - request: Запрос пользователя.

        Возвращает:
            - HttpResponse: Ответ на запрос с перенаправлением на главную страницу.
        """
        try:
            outstanding_token = OutstandingToken.objects.filter(
                user=request.user).last()
            ic(outstanding_token)
            outstanding_token.delete()
        except (OutstandingToken.DoesNotExist, AttributeError):
            pass
        logout(request)

        resp = HttpResponse()
        resp.delete_cookie(key='access_token')
        return HttpResponseRedirect(reverse('pages:mainpage'))


# APIS
class RegisterAPIView(APIView):
    """
    Класс для регистрации нового пользователя через API.

    Методы:
        post() - Обрабатывает POST-запрос на регистрацию нового пользователя.
    """

    def post(self, request):
        """
        Обрабатывает POST-запрос на регистрацию нового пользователя.

        Параметры:
            - request: Запрос пользовательского API.

        Возвращает:
            - Response: Ответ на запрос с данными ново зарегистрированного пользователя.
        """
        serializer = UserSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
