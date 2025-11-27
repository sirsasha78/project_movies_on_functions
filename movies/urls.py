from django.urls import path
from . import views


app_name = "movies"


urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path("search/", views.MovieSearch.as_view(), name="movie_search"),
    path("tag/<str:tag_slug>/", views.MovieList.as_view(), name="movie_list_by_tag"),
    path("addmovie/", views.AddMovie.as_view(), name="add_movie"),
    path("<slug:slug>/update", views.MovieUpdateView.as_view(), name="movie_update"),
    path("<int:movie_id>/", views.MovieShare.as_view(), name="movie_share"),
    path("<int:movie_id>/comment/", views.MovieComment.as_view(), name="movie_comment"),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
]
