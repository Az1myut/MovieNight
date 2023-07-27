from django.urls import path
from .views import (
    RegisterAPIView,
    RegisterView,
    LoginView,
    LogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    EmailConfirmTemplateView,
    NewPasswordTemplateView
)

app_name = 'registration'
urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register_api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('email/confirm/', EmailConfirmTemplateView.as_view(), name='email_confirm'),
    path('password/new/', NewPasswordTemplateView.as_view(), name='new_password'),
]