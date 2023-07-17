"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('registration/',include('registration.urls',namespace='registration.registration')),
    path('movies/',include('movies.urls',namespace='movies.movies')),
    path('actors/',include('actors.urls',namespace='actors.actors')),
    path('articles/', include('articles.urls', namespace ='articles.articles')),
    path('contacts/',include('contacts.urls',namespace='contacts.contacts')),
    #JWT URLs START
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    #JWT URLS END
    #CAPTCHA
    path('captcha/', include('captcha.urls')),
    
    path('', include('pages.urls', namespace='pages.pages')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
