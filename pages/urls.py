from django.urls import path
from .views import (
    MainpageTemplateView,
    FilteredMoviesListView,
    filter_movies,
    ProfileTemplateView,
    search_movies,
    SearchResultsListView,
    UserArticlesListView,
    UserFavoriteMoviesListView,
    UserFavoriteMoviesAddDetailView,
    UserFavoriteMoviesRemoveDetailView
)
app_name = 'pages'
urlpatterns = [
    path('filter/movies/', filter_movies, name='filter_movies'),
    path('filtered/<int:option>/movies/',FilteredMoviesListView.as_view(), name='filtered_movies'),
    path('profile/', ProfileTemplateView.as_view(), name='profile_page'),
    path('search/', search_movies, name='search_movies'),
    path('search/<str:query>', SearchResultsListView.as_view(), name='search_results'),
    path('my/articles/', UserArticlesListView.as_view(), name='user_articles'),
    path('my/favorites/', UserFavoriteMoviesListView.as_view(), name='user_favorites'),
    path('my/favorites/<int:pk>/add/', UserFavoriteMoviesAddDetailView.as_view(), name='user_favorites_add'),
    path('my/favorites/<int:pk>/remove/', UserFavoriteMoviesRemoveDetailView.as_view(), name='user_favorites_remove'),
    path('', MainpageTemplateView.as_view(), name='mainpage'),
]           