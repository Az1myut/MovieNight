from django.urls import path
from .views import(
    ShowActorPageDetailView,
   
)
app_name = 'actors'

urlpatterns = [
    path('detail/<int:pk>', ShowActorPageDetailView.as_view(), name = 'actor_detail'),

]