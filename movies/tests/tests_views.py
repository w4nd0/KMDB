from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import User
from movies.models import Movies
from movies.serializers import MovieSerializer


class MovieViewTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admim_user_test",
            password="1234",
            first_name="admim",
            last_name="test",
        )

        self.token_admim = Token.objects.create(user=self.admin_user)

        self.critico_user = User.objects.create_user(
            username="critico_user_test",
            password="1234",
            first_name="critico",
            last_name="test",
            is_superuser=False,
            is_staff=True,
        )

        self.token_critico = Token.objects.create(user=self.critico_user)

        self.comum_user = User.objects.create_user(
            username="comum_user_test",
            password="1234",
            first_name="user",
            last_name="test",
            is_superuser=False,
            is_staff=False,
        )

        self.token_user = Token.objects.create(user=self.comum_user)

        self.movie_data = {
            "title": "movie test",
            "duration": "175m",
            "genres": [{"name": "test"}],
            "premiere": "1972-09-10",
            "classification": 15,
            "synopsis": "synopsis test",
        }

        self.update_movie_data = {
            "title": "movie update test",
            "duration": "175m",
            "genres": [{"name": "test"}],
            "premiere": "1972-09-10",
            "classification": 15,
            "synopsis": "synopsis test",
        }

    # POST
    def test_create_new_movie_as_admim(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.post("/api/movies/", self.movie_data, format="json")

        self.assertEqual(response.status_code, 201)

    def test_create_new_movie_without_permission(self):
        response = self.client.post("/api/movies/", self.movie_data, format="json")

        self.assertEqual(response.status_code, 401)

    def test_create_new_movie_with_wrong_request_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.post(
            "/api/movies/", {"title": "wrong entry"}, format="json"
        )

        self.assertEqual(response.status_code, 422)

    def test_critico_cannot_create_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.post("/api/movies/", self.movie_data, format="json")

        self.assertEqual(response.status_code, 403)

    def test_comum_user_cannot_create_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.post("/api/movies/", self.movie_data, format="json")

        self.assertEqual(response.status_code, 403)

    # GET
    def test_list_movies(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        response = self.client.get("/api/movies/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), Movies.objects.count())

        self.assertIn(movie.data, response.data)

    def test_list_movies_empty(self):
        response = self.client.get("/api/movies/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_can_read_a_specific_film_with_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.get(f"/api/movies/{movie.data['id']}/")
        
        self.assertEquals(response.status_code, 200)

        self.assertIsNotNone(response.json().get("reviews"))

        self.assertEquals(movie.data, response.data)

    def test_can_read_a_specific_film_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token")

        response = self.client.get(f"/api/movies/{movie.data['id']}/")

        self.assertIsNone(response.json().get("reviews"))

        self.assertEquals(response.status_code, 401)

        self.assertEquals(movie.data, response.data)

    def test_read_a_specific_film_with_wrong_id(self):
        response = self.client.get("/api/movies/50/")

        self.assertEquals(response.status_code, 404)

    # PATCH
    def test_update_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")       

        response = self.client.put(
            f"/api/movies/{movie.data['id']}/", self.update_movie_data, format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_update_movie_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json") 

        self.client.credentials(HTTP_AUTHORIZATION="Token")

        response = self.client.put(
            f"/api/movies/{movie.data['id']}/", self.update_movie_data, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_update_movie_with_wrong_request_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json") 

        response = self.client.put(
            f"/api/movies/{movie.data['id']}/", {"title": "wrong entry"}, format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_update_movie_with_wrong_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.put(
            "/api/movies/50/", self.update_movie_data, format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_critico_cannot_update_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.put(
            f"/api/movies/{movie.data['id']}/", self.update_movie_data, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_comum_user_cannot_update_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.put(
            f"/api/movies/{movie.data['id']}/", self.update_movie_data, format="json"
        )

        self.assertEqual(response.status_code, 403)

    # DELETE
    def test_delete_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        response = self.client.delete(f"/api/movies/{movie.data['id']}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_movie_with_wrong_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.put("/api/movies/50/")

        self.assertEqual(response.status_code, 404)

    def test_delete_movie_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token")

        response = self.client.delete(f"/api/movies/{movie.data['id']}/")

        self.assertEqual(response.status_code, 401)

    def test_critico_cannot_delete_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.delete(f"/api/movies/{movie.data['id']}/")

        self.assertEquals(response.status_code, 403)

    def test_comum_user_cannot_delete_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.delete(f"/api/movies/{movie.data['id']}/")

        self.assertEquals(response.status_code, 403)


class ReviewModelTest(APITestCase):
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

        cls.admin_user = User.objects.create_superuser(
            username="admim_user_test",
            password="1234",
            first_name="admim",
            last_name="test",
        )

        cls.token_admim = Token.objects.create(user=cls.admin_user)

        cls.critico_user = User.objects.create_user(
            username="critico_user_test",
            password="1234",
            first_name="critico",
            last_name="test",
            is_superuser=False,
            is_staff=True,
        )

        cls.token_critico = Token.objects.create(user=cls.critico_user)

        cls.comum_user = User.objects.create_user(
            username="comum_user_test",
            password="1234",
            first_name="user",
            last_name="test",
            is_superuser=False,
            is_staff=False,
        )

        cls.token_user = Token.objects.create(user=cls.comum_user)

        cls.review = {"stars": 7, "review": "test review", "spoilers": False}

        cls.update_review = {
            "stars": 5,
            "review": "test update review",
            "spoilers": False,
        }

    # POST
    def test_critico_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_critic_cannot_create_review_twice_for_same_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 422)

    def test_create_review_without_authorization(self):
        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_create_review_without_with_wrong_request_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/",
            {"stars": "wrong entry"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_with_wrong_movie_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.post(
            "/api/movies/50/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_comum_user_cannot_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_admim_user_cannot_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", self.review, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_cannot_create_review_with_stars_out_from_1_to_10(self):
        review1 = {"stars": 15, "review": "test review", "spoilers": False}

        review2 = {"stars": -5, "review": "test review", "spoilers": False}

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", review1, format="json"
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            f"/api/movies/{self.movie.id}/review/", review2, format="json"
        )

        self.assertEqual(response.status_code, 400)

    # GET
    def test_list_reviews_as_admim(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)

    def test_list_reviews_as_critico(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)

        for review in response.data:
            self.assertEqual(review.critic.id, self.critico_user.id)

    def test_list_reviews_without_permission(self):
        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 401)

    def test_list_reviews_as_comum_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.get("/api/reviews/")

        self.assertEqual(response.status_code, 403)

    # PATCH
    def test_critico_can_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.put(
            f"/api/movies/{self.movie.id}/review/", self.update_review, format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_update_review_without_authorization(self):
        response = self.client.put(
            f"/api/movies/{self.movie.id}/review/", self.update_review, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_update_review_without_with_wrong_request_format(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.put(
            f"/api/movies/{self.movie.id}/review/",
            {"stars": "wrong entry"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_update_review_with_wrong_movie_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_critico.key}")

        response = self.client.put(
            f"/api/movies/50/review/", self.update_review, format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_comum_user_cannot_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_user.key}")

        response = self.client.put(
            f"/api/movies/{self.movie.id}/review/", self.update_review, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_admim_user_cannot_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admim.key}")

        response = self.client.put(
            f"/api/movies/{self.movie.id}/review/", self.update_review, format="json"
        )

        self.assertEqual(response.status_code, 403)
