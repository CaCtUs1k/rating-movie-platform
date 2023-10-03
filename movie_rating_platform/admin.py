from django.contrib import admin

from movie_rating_platform.models import Genre, Movie, Visitor, Rating, Like


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    filter_horizontal = ("genres",)


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    filter_horizontal = ("wishlist",)


admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Like)
