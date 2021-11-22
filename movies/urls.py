from django.urls import path
from rest_framework import routers

from movies.views import MovieView, ReviewView, MovieReviewView

router = routers.SimpleRouter()

router.register(r'movies', MovieView, basename='movies')
router.register(r'reviews', ReviewView, basename='reviews')

urlpatterns = [path("movies/<int:pk>/review/", MovieReviewView.as_view()),]

urlpatterns += router.urls
