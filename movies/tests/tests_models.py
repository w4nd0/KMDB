from django.test import TestCase

from movies.models import Movies, Genres, Review
from accounts.models import User


class MoviesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.title = "movie test"
        cls.duration = "175m"
        cls.premiere = "1972-09-10"
        cls.classification = 15
        cls.synopsis = "synopsis test"

        cls.movie = Movies.objects.create(
            title=cls.title,
            duration=cls.duration,
            premiere=cls.premiere,
            classification=cls.classification,
            synopsis=cls.synopsis,
        )


        cls.username = "user"
        cls.password = "1234"
        cls.first_name = "test"
        cls.last_name = "test"

        cls.user = User.objects.create_superuser(
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )

        cls.stars = 5
        cls.review = "review test"
        cls.spoilers = False

        cls.test_review = Review.objects.create(
            stars=cls.stars,
            review=cls.review,
            spoilers=cls.spoilers,
            movie=cls.movie,
            critic=cls.user
        )

    def test_movie_has_information_fields(self):
        self.assertIsInstance(self.movie.title, str)
        self.assertEqual(self.movie.title, self.title)

        self.assertIsInstance(self.movie.duration, str)
        self.assertEqual(self.movie.duration, self.duration)

        self.assertIsInstance(self.movie.premiere, str)
        self.assertEqual(self.movie.premiere, self.premiere)

        self.assertIsInstance(self.movie.classification, int)
        self.assertEqual(self.movie.classification, self.classification)

        self.assertIsInstance(self.movie.synopsis, str)
        self.assertEqual(self.movie.synopsis, self.synopsis)

    def test_genre_movie_relationship(self):
        genres = [Genres.objects.create(name=f"Genre {i}") for i in range(3)]

        for genre in genres:
            self.movie.genres.add(genre)

        self.assertEqual(len(genres), self.movie.genres.count())

    def test_review_has_information_fields(self):
        self.assertIsInstance(self.test_review.stars, int)
        self.assertEqual(self.test_review.stars, self.stars)

        self.assertIsInstance(self.test_review.review, str)
        self.assertEqual(self.test_review.review, self.review)

        self.assertIsInstance(self.test_review.spoilers, bool)
        self.assertEqual(self.test_review.spoilers, self.spoilers)

    def test_review_movie_relationship(self):
        Review.objects.create(
            stars=self.stars,
            review=self.review,
            spoilers=self.spoilers,
            movie=self.movie,
        )

        #2 pois já tem uma review criada no setUpTestData
        self.assertEquals(self.movie.reviews.count(), 2)

    def test_review_user_relationship(self):
        review_test = Review.objects.create(
            stars=self.stars, review=self.review, spoilers=self.spoilers, critic=self.user
        )

        review_test.id = self.test_review.id

        self.assertEquals(review_test, self.test_review)


class GenresModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = "test"

        cls.genre = Genres.objects.create(name=cls.name)

    def test_genre_has_information_fields(self):
        self.assertIsInstance(self.genre.name, str)
        self.assertEqual(self.genre.name, self.name)
