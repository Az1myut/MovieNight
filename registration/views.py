from django.shortcuts import render, redirect
from django.urls import reverse_lazy, resolve, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerialzer
from .forms import LoginForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import User
from users.forms import EmailForm
from django.views.generic.base import TemplateView, View
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from icecream import ic
import requests
import datetime
import random
import string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
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

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_message = 'Your password was successfully updated'
    success_url = reverse_lazy('pages:profile_page')
    template_name  = 'registration/password_change.html'

class CustomPasswordResetView(TemplateView):
    template_name = 'registration/password_reset.html'
    form_class = EmailForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmailForm
        return context
    def generate_random_string(self):
        random_chars = random.choices(string.ascii_lowercase + string.digits, k=6)
        random_string = ''.join(random_chars)
        return random_string

    def send_code_for_password_reset(self, to_email, code):
        send_mail(
            subject= 'Reset Password',
            message= f'Your code is {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list= [to_email,],
            fail_silently=False,
        )

    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        context = self.get_context_data()
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
                expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
                code = self.generate_random_string()
                response = HttpResponseRedirect(reverse('registration:email_confirm'))
                response.set_cookie('code', code, httponly=True,expires=expiration_date)
                response.set_cookie('email', email, httponly=True,expires=expiration_date)
                self.send_code_for_password_reset(to_email=email, code=code)
                
                return response
            except User.DoesNotExist:
                messages.error(request, 'There is no such email')
                context['form'] = form
                return render(request, self.template_name, context=context)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pages:mainpages')
        return super().get(request, *args, **kwargs)
class EmailConfirmTemplateView(TemplateView):
    template_name = 'registration/email_confirm.html'

    def get(self, request, *args, **kwargs):
        if request.COOKIES.get('code'):
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse("You should first enter email to get code for password reset", status=409)

    def post(self, request, *args, **kwargs):
        cookie_code = request.COOKIES.get('code')
        form_code = request.POST.get('code')
        if cookie_code == form_code:
            expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
            response = HttpResponseRedirect(reverse('registration:new_password'))
            response.set_cookie('email_check', 'true', httponly=True,expires=expiration_date)
            return response
        else:
            messages.error(request,'Wrong code')
            return render(request, self.template_name)

class NewPasswordTemplateView(TemplateView):
    template_name = 'registration/new_password.html'

    def get(self, request, *args, **kwargs):
        email_check = request.COOKIES.get('email_check')
        if email_check == 'true':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse("You should first confirm email", status=409)
    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 != password2:
            messages.error(request, 'Password dont match')
            return self.get(request, *args, **kwargs)
        try:
            validate_password(password1)
        except ValidationError as errors:
            for error in errors:
                messages.error(request,error)
            return self.get(request, *args, **kwargs)
        email = request.COOKIES.get('email')
        ic(email)
        user = User.objects.get(email=email)
        user.set_password(password1)
        user.save()
        
        response = HttpResponseRedirect(reverse('registration:login'))
        response.delete_cookie('check_email')
        response.delete_cookie('email')
        response.delete_cookie('code')
        messages.success(request,'New Password Was Set' )
        
        return response
        

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
