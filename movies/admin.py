from django.contrib import admin
from .models import Movie, Genre, Director, Comment


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "director")
    list_filter = ("year", "rating", "director", "genre")
    search_fields = ("title", "description")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "movie", "created", "active")
    list_filter = ("active", "created", "updated")
    search_fields = ("name", "email", "body")
