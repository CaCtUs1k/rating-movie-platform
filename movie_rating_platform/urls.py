from django.urls import path


app_name = "movie_rating"

urlpatterns = [
    path("", index, name="index"),
]