import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from movie_rating_platform.utils.utils_model import custom_title


class Genre(models.Model):
    name = models.CharField(
        max_length=63,
        unique=True,
        error_messages={"unique": "This genre already exists"},
    )

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    release_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1895),
            MaxValueValidator(datetime.datetime.now().year),
        ]
    )
    poster_link = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre, "movies")

    def save(self, *args, **kwargs):
        self.title = custom_title(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Visitor(AbstractUser):
    wishlist = models.ManyToManyField(
        Movie,
        "users",
    )

    def get_absolute_url(self):
        return reverse("movie_rating:visitor-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username}"


class Rating(models.Model):
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    description = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(
        Visitor, on_delete=models.DO_NOTHING, related_name="ratings"
    )
    create_time = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="ratings"
    )

    def __str__(self):
        return self.description


class Like(models.Model):
    sender = models.ForeignKey(
        Visitor, on_delete=models.DO_NOTHING, related_name="likes"
    )
    target = models.ForeignKey(
        Movie, on_delete=models.DO_NOTHING, related_name="likes"
    )
