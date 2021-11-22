from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework import mixins

from rest_framework.viewsets import GenericViewSet, ModelViewSet

from utils.permissions import IsCriticoUser, IsSuperUserOrReadOnly

from movies.models import Movies, Review
from movies.serializers import MovieSerializer, ReviewSerializer, MovieWithReviewSerializer

class SearchForTitle(filters.SearchFilter):
    search_param = "title"

class MovieView(ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

    filter_backends = [SearchForTitle]
    search_fields = ["title"]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user     

        if not user.is_anonymous and self.request.method != 'POST':
            return MovieWithReviewSerializer
        
        return super().get_serializer_class()


class ReviewView(mixins.ListModelMixin, GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCriticoUser]

    def filter_queryset(self, queryset):
        if self.request.user.is_superuser:
            queryset = Review.objects.all()
        else:
            queryset = queryset.filter(critic_id=self.request.user.id)

        return super().filter_queryset(queryset)


class MovieReviewView(UpdateAPIView, CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCriticoUser]

    def create(self, request, *args, **kwargs):
        movie = get_object_or_404(Movies, id=kwargs.get("pk"))

        request.data["movie"] = movie.id

        return super().create(request, *args, **kwargs)
