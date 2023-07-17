from django.urls import path
from .views import (
    ShowMoviePageDetailView,
    MovieActorsListView,
    ShowLatestMoviesListView,
    ShowUpcomingMoviesListView,
    ShowMonthTopMoviesListView,
    UserRateMovieDetailView,
    UserDeleteRateMovieDetailView,
    UserLikeUnlikeMovie,
)
app_name = 'movies'
urlpatterns = [
    path('detail/<int:pk>', ShowMoviePageDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/actors', MovieActorsListView.as_view(), name='movie_actors'),
    path('<int:pk>/rate', UserRateMovieDetailView.as_view(), name='user_movie_rate'),
    path('<int:pk>/rate/delete', UserDeleteRateMovieDetailView.as_view(), name='user_movie_rate_delete'),
    path('<int:pk>/<str:action>', UserLikeUnlikeMovie.as_view(), name='user_movie_like_unlike'),
    path('latest', ShowLatestMoviesListView.as_view(), name='latest_movies'),    
    path('upcoming', ShowUpcomingMoviesListView.as_view(), name='upcoming_movies'),
    path('month-top', ShowMonthTopMoviesListView.as_view(), name='month_top_movies'),  

]