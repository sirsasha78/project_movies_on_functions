from django.contrib import admin
from .models import Movie, Genre, Director


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "genre", "director")
    list_filter = ("year", "rating", "director", "genre")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("last_name",)}
