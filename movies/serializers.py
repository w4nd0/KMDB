import ipdb
from accounts.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movies.models import Genres, Movies, Review

ValidationError.status_code = 422

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ["id", "name"]

class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
        
class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        
        extra_kwargs = {
            'movie': {'write_only': True}
        }

    def create(self, validated_data):
        check_already_reviewed = Review.objects.filter(critic_id=self.context["request"].user.id).filter(movie_id=validated_data['movie'].id)

        if check_already_reviewed:
            raise ValidationError({"detail": "You already made this review."})

        return Review.objects.create(
            **validated_data, critic=self.context["request"].user
        )

    def update(self, instance, validated_data):
        validated_data["critic"] = self.context["request"].user
        return super().update(instance, validated_data)

class MovieWithReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    genres = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Movies
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(many=True)
    class Meta:
        model = Movies
        fields = "__all__"

    def create(self, validated_data):
        genres = validated_data.pop("genres")
        movie = Movies.objects.create(**validated_data)

        for genre in genres:
            get_genre = Genres.objects.filter(name=genre["name"]).first()
            if get_genre:
                movie.genres.add(get_genre)
            else:
                new_genre = Genres.objects.create(**genre)
                movie.genres.add(new_genre)

        return movie

    def update(self, instance, validated_data):
        genres = validated_data.pop("genres")

        for genre in genres:
            get_genre = Genres.objects.filter(name=genre["name"]).first()
            if get_genre:
                instance.genres.add(get_genre)
            else:
                new_genre = Genres.objects.create(**genre)
                instance.genres.add(new_genre)

        return super().update(instance, validated_data)





