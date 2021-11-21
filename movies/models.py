from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Movies(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    premiere = models.CharField(max_length=255)
    classification = models.IntegerField()
    synopsis = models.CharField(max_length=511)


class Review(models.Model):
    stars = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    review = models.TextField()
    spoilers = models.BooleanField()

    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, null=True, related_name="reviews"
    )
    critic = models.ForeignKey("accounts.User", on_delete=models.PROTECT, null=True)


class Genres(models.Model):
    name = models.CharField(max_length=255)

    movies = models.ManyToManyField(Movies, related_name="genres")
