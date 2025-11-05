from django.urls import path
from . import views


app_name = "movies"


urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("tag/<str:tag_slug>/", views.movie_list, name="movie_list_by_tag"),
    path("addmovie/", views.add_movie, name="add_movie"),
    path("<int:movie_id>/", views.movie_share, name="movie_share"),
    path("<int:movie_id>/comment/", views.movie_comment, name="movie_comment"),
    path("<slug:slug>/", views.movie_detail, name="movie_detail"),
]
