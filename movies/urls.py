from django.urls import path

from movies.views import MovieView, RetrieveMovieView, ReviewView, MovieReviewView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:pk>/", RetrieveMovieView.as_view()),
    path("reviews/", ReviewView.as_view()),
    path("movies/<int:pk>/review/", MovieReviewView.as_view()),
]
