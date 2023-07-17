from django.urls import path
from .views import (
    RegisterAPIView,
    RegisterView,
    LoginView,
    LogoutView
    
)

app_name = 'registration'
urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='register_api'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]