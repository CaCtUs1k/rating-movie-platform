from django.urls import path

from movie_rating_platform.views import (
    index,
    MovieListView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    VisitorListView,
    VisitorDetailView,
    VisitorCreateView,
    VisitorUpdateView,
    VisitorDeleteView,
    movie_detail_view,
    create_rating_view,
    RatingUpdateView,
    RatingDeleteView,
    toggle_assign_to_movie,
    register,
    change_avatar,
)

app_name = "movie_rating"

urlpatterns = [
    path("register/", register, name="register"),
    path("", index, name="index"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/create/", MovieCreateView.as_view(), name="movie-create"),
    path("movies/<int:pk>/", movie_detail_view, name="movie-detail"),
    path(
        "movies/<int:pk>/toggle_wishlist/",
        toggle_assign_to_movie,
        name="toggle_wishlist",
    ),
    path(
        "movies/<int:movie_pk>/rating/<int:pk>/update/",
        RatingUpdateView.as_view(),
        name="rating-update",
    ),
    path(
        "movies/<int:movie_pk>/rating/<int:pk>/delete/",
        RatingDeleteView.as_view(),
        name="rating-delete",
    ),
    path(
        "movies/<int:pk>/rating/create/",
        create_rating_view,
        name="rating-create",
    ),
    path(
        "movies/<int:pk>/update/",
        MovieUpdateView.as_view(),
        name="movie-update",
    ),
    path(
        "movies/<int:pk>/delete/",
        MovieDeleteView.as_view(),
        name="movie-delete",
    ),
    path("users/", VisitorListView.as_view(), name="visitor-list"),
    path("users/create/", VisitorCreateView.as_view(), name="visitor-create"),
    path(
        "users/<int:pk>/", VisitorDetailView.as_view(), name="visitor-detail"
    ),
    path("users/<int:pk>/update_avatar/", change_avatar, name="avatar-change"),
    path(
        "users/<int:pk>/update/",
        VisitorUpdateView.as_view(),
        name="visitor-update",
    ),
    path(
        "users/<int:pk>/delete/",
        VisitorDeleteView.as_view(),
        name="visitor-delete",
    ),
]
