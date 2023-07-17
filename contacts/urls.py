from django.urls import path
from .views import ContactPageTemplateView
app_name = 'contacts'

urlpatterns = [
    path('',ContactPageTemplateView.as_view(), name='contact_page')
]
