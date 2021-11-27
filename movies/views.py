from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from utils.mixins import CreateUpdateViewSet
from utils.permissions import IsCriticoUser, IsSuperUserOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from movies.models import Movies, Review
from movies.serializers import (
    MovieSerializer,
    MovieWithReviewSerializer,
    ReviewSerializer,
)


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

        if not user.is_anonymous and self.request.method != "POST":
            return MovieWithReviewSerializer

        return super().get_serializer_class()

    def get_object(self):
        user = self.request.user

        if self.action == "review":
            return Review.objects.filter(critic_id=user.id, movie_id=self.kwargs["pk"])

        return super().get_object()

    @action(
        methods=["post", "put"],
        detail=True,
        permission_classes=[IsCriticoUser],
        serializer_class=ReviewSerializer,
    )
    def review(self, request, *args, **kwargs):
        movie = get_object_or_404(Movies, id=kwargs["pk"])

        if request.method == "POST":
            request.data["movie"] = movie.id

            return super().create(request, *args, **kwargs)

        else:
            review = self.get_object()
            request.data["critic"] = self.request.user

            review.update(**request.data)

            try:
                serializer = ReviewSerializer(review[0])

                return Response(serializer.data, status=status.HTTP_200_OK)

            except IndexError:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )


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


class MovieReviewView(CreateUpdateViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCriticoUser]

    def create(self, request, *args, **kwargs):
        movie = get_object_or_404(Movies, id=kwargs["pk"])

        request.data["movie"] = movie.id

        return super().create(request, *args, **kwargs)
