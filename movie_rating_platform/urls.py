from django.urls import path

from movie_rating_platform.views import index, MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, \
    MovieDeleteView

app_name = "movie_rating"

urlpatterns = [
    path("", index, name="index"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("movies/create/", MovieCreateView.as_view(), name="movie-create"),
    path("movies/<int:pk>/update/", MovieUpdateView.as_view(), name="movie-update"),
    path("movies/<int:pk>/delete/", MovieDeleteView.as_view(), name="movie-delete"),
]