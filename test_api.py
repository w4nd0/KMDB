from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model


class TestMovieView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "premiere": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "premiere": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_admin_can_create_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")
        self.assertEqual(movie.json()["id"], 1)
        self.assertEqual(movie.status_code, 201)

    def test_critic_cannot_create_movie(self):
        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot create movie
        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

    def test_user_cannot_create_movie(self):
        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user cannot create movie
        status_code = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).status_code

        self.assertEqual(status_code, 403)

    def test_anonymous_cannot_create_movie(self):
        # anonymous user create movie
        response = self.client.post("/api/movies/", self.movie_data, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_anonymous_can_list_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # list movies
        movies_list = client.get("/api/movies/", format="json").json()
        self.assertEqual(len(movies_list), 1)

    def test_genre_cannot_repeat(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie 1
        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        # create movie 2
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_2, format="json"
        ).json()
        # testa se os ids do gênero drama são os mesmos
        self.assertEqual(movie_1["genres"][1]["id"], movie_2["genres"][0]["id"])

    def test_filter_movies_with_the_filter_request(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie 1
        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        # create movie 2
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_2, format="json"
        ).json()

        # create movie 3
        movie_2 = self.client.post(
            "/api/movies/", self.movie_data_3, format="json"
        ).json()

        # filter movies
        filter_movies = self.client.get("/api/movies/?title=liberdade")

        self.assertEqual(len(filter_movies.json()), 2)
        self.assertEqual(filter_movies.status_code, 200)

    def test_output_format_data(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie 1
        movie_1 = self.client.post(
            "/api/movies/", self.movie_data, format="json"
        ).json()

        output_format_movie_data = {
            "id": 1,
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"id": 1, "name": "Crime"}, {"id": 2, "name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.assertEqual(movie_1, output_format_movie_data)

    def test_only_admin_can_update_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")
        self.assertEqual(movie.json()["id"], 1)
        self.assertEqual(movie.json()["title"], "O Poderoso Chefão")
        self.assertEqual(movie.status_code, 201)

        # update movie
        movie = self.client.put("/api/movies/1/", self.movie_data_2, format="json")
        self.assertEqual(movie.json()["id"], 1)
        self.assertEqual(movie.json()["title"], "Um Sonho de liberdade")
        self.assertEqual(movie.status_code, 200)

    def test_critic_cannot_update_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        self.client.post("/api/movies/", self.movie_data, format="json")

        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot create movie
        status_code = self.client.put(
            "/api/movies/1/", self.movie_data_2, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

    def test_user_cannot_update_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        self.client.post("/api/movies/", self.movie_data, format="json")

        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user cannot create movie
        status_code = self.client.put(
            "/api/movies/1/", self.movie_data_2, format="json"
        ).status_code

        self.assertEqual(status_code, 403)

    def test_anonymous_cannot_update_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        self.client.post("/api/movies/", self.movie_data, format="json")

        # remove admin credetials
        self.client.credentials()

        # anonymous user create movie
        response = self.client.put("/api/movies/1/", self.movie_data_2, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )


class TestMovieRetrieveDestroyView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "username": "user",
            "first_name": "Edward",
            "last_name": "Stewart",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False,
        }

        self.user_login_data = {"username": "user", "password": "1234"}

        self.critic_data = {
            "username": "critic",
            "first_name": "Erick",
            "last_name": "Jacquin",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False,
        }

        self.critic_login_data = {"username": "critic", "password": "1234"}

        self.admin_data = {
            "username": "admin",
            "first_name": "Jeff",
            "last_name": "Bezos",
            "password": "1234",
            "is_staff": True,
            "is_superuser": True,
        }

        self.admin_login_data = {"username": "admin", "password": "1234"}

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de liberdade",
            "duration": "142m",
            "genres": [{"name": "Ficção Científica"}, {"name": "Drama"}],
            "premiere": "1994-10-14",
            "classification": 14,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }

        self.movie_data_3 = {
            "title": "Em busca de liberdade",
            "duration": "175m",
            "genres": [{"name": "Obra de época"}, {"name": "Drama"}],
            "premiere": "2018-02-22",
            "classification": 14,
            "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell (Joseph Fiennes) ganha uma medalha de ouro nas Olimpíadas de Paris em 1924. Ele decide ir até a China para trabalhar como missionário e acaba encontrando um país em guerra. Com a invasão japonesa no território chinês durante a Segunda Guerra Mundial, Liddell acaba em um campo de concentração.",
        }

    def test_anonymous_can_filter_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movies
        self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # filter movie 1
        movies_filter = client.get("/api/movies/1/", format="json")

        self.assertEqual(movies_filter.status_code, 200)
        self.assertEqual(movies_filter.json()["id"], 1)

    def test_anonymous_cannot_filter_movies_with_the_invalid_movie_id(self):
        # filter movie 99
        movies_filter = self.client.get("/api/movies/99/", format="json")
        self.assertEqual(movies_filter.status_code, 404)
        self.assertEqual(movies_filter.json(), {"detail": "Not found."})

    def test_critic_cannot_delete_movies(self):
        # create critic user
        self.client.post("/api/accounts/", self.critic_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic cannot delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)

    def test_user_cannot_delete_movies(self):
        # create user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # user cannot delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 403)

    def test_anonymous_cannot_delete_movies(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # delete movie
        movie_delete = client.delete("/api/movies/1/", format="json")
        self.assertEqual(movie_delete.status_code, 401)
        self.assertEqual(
            movie_delete.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_admin_can_delete_movie(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        # get movies
        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 1)

        # delete movie
        status_code = self.client.delete("/api/movies/1/", format="json").status_code
        self.assertEqual(status_code, 204)

        # get movies
        movies = self.client.get("/api/movies/", format="json")
        self.assertEqual(len(movies.json()), 0)
        self.assertEqual(movies.json(), [])

    def test_anonymous_filter_movie_without_critic(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movies
        self.client.post("/api/movies/", self.movie_data, format="json")

        # reset client -> no login
        client = APIClient()

        # filter movie 1
        movies_filter = client.get("/api/movies/1/", format="json")

        self.assertEqual(movies_filter.status_code, 200)
        self.assertEqual(movies_filter.json()["id"], 1)
        self.assertNotIn("reviews", movies_filter.json())

    def test_user_filter_movie_with_critic(self):
        # create admin user
        self.client.post("/api/accounts/", self.admin_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movies
        self.client.post("/api/movies/", self.movie_data, format="json")

        # change to user
        # create critic user
        self.client.post("/api/accounts/", self.user_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # filter movie 1
        movies_filter = self.client.get("/api/movies/1/", format="json")

        self.assertEqual(movies_filter.status_code, 200)
        self.assertEqual(movies_filter.json()["id"], 1)
        self.assertIn("reviews", movies_filter.json())


class TestAccountView(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
        }

        self.user_login_data = {
            "username": "user",
            "password": "1234",
        }

        self.critic_data = {
            "username": "critic",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": True,
        }

        self.critic_login_data = {
            "username": "critic",
            "password": "1234",
        }

        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": True,
            "is_staff": True,
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234",
        }

        self.wrong_admin_login_data = {
            "username": "admin",
            "password": "12345",
        }

    def test_create_and_login_for_user_account(self):
        client = APIClient()
        # create user
        user = client.post("/api/accounts/", self.user_data, format="json").json()

        self.assertEqual(
            user,
            {
                "id": 1,
                "username": "user",
                "is_superuser": False,
                "is_staff": False,
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        # login
        response = client.post(
            "/api/login/", self.user_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_critic_account(self):
        client = APIClient()
        # create user
        user = client.post("/api/accounts/", self.critic_data, format="json").json()

        self.assertEqual(
            user,
            {
                "id": 1,
                "username": "critic",
                "is_superuser": False,
                "is_staff": True,
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        # login
        response = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_admin_account(self):
        client = APIClient()
        # create user
        user = client.post("/api/accounts/", self.admin_data, format="json").json()

        self.assertEqual(
            user,
            {
                "id": 1,
                "username": "admin",
                "is_superuser": True,
                "is_staff": True,
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        # login
        response = client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_user_already_exists(self):

        client = APIClient()
        # create user
        client.post("/api/accounts/", self.admin_data, format="json")
        response = client.post("/api/accounts/", self.admin_data, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"username": ["A user with that username already exists."]}
        )

    def test_login_non_existing_user(self):
        client = APIClient()

        # try to login with non existing user
        response = client.post("/api/login/", self.admin_login_data, format="json")

        self.assertEqual(response.status_code, 401)

    def test_wrong_credentials_do_not_login(self):
        client = APIClient()

        # create user
        client.post("/api/accounts/", self.admin_data, format="json").json()

        # login with wrong password
        response = client.post(
            "/api/login/", self.wrong_admin_login_data, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_missing_login_data(self):
        client = APIClient()

        # create user
        client.post("/api/accounts/", self.admin_data, format="json").json()

        # login with wrong password
        response = client.post("/api/login/", {"username": "critic"}, format="json")

        self.assertEqual(response.status_code, 400)


class TestCriticismReviewView(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
        }

        self.user_login_data = {
            "username": "user",
            "password": "1234",
        }

        self.critic_data = {
            "username": "critic",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": True,
        }

        self.critic_login_data = {
            "username": "critic",
            "password": "1234",
        }

        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": True,
            "is_staff": True,
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234",
        }

        self.movie_data_1 = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.movie_data_2 = {
            "title": "Um Sonho de Liberdade",
            "duration": "142m",
            "genres": [{"name": "Drama"}, {"name": "Ficção científica"}],
            "premiere": "1994-10-14",
            "classification": 16,
            "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas consecutivas pelas mortes de sua esposa e de seu amante. Porém, só Andy sabe que ele não cometeu os crimes. No presídio, durante dezenove anos, ele faz amizade com Red, sofre as brutalidades da vida na cadeia, se adapta, ajuda os carcereiros, etc.",
        }
        self.review_data_1 = {
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.review_data_2 = {
            "stars": 10,
            "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
            "spoilers": True,
        }

        self.wrong_review_data = {
            "stars": 20,
            "review": "Muito fraco",
            "spoilers": False,
        }

    def test_create_review_without_movie(self):
        client = APIClient()

        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # trying to create critic review without movie
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_admin_cannot_create_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # admin trying to create critic review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_create_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create regular user
        client.post("/api/accounts/", self.user_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with regular user
        token = client.post("/api/login/", self.user_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # regular user trying to create critic review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 403)

    def test_critic_can_create_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user trying to create review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        expected_review_response = {
            "id": 1,
            "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_review_response)

        # verifying if criticism is nested with movie
        response = client.get("/api/movies/1/").json()
        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 2,
                "review": "Muito fraco",
                "spoilers": False,
            }
        ]
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)

    def test_critic_cannot_duplicate_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()
        # create regular user
        client.post("/api/accounts/", self.user_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user trying to create review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        expected_review_response = {
            "id": 1,
            "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_review_response)

        expected_review_response = {"detail": "You already made this review."}

        # critic user trying to create same review as before
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), expected_review_response)

        # verifying if criticism is nested with movie
        response = client.get("/api/movies/1/").json()

        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 2,
                "review": "Muito fraco",
                "spoilers": False,
            }
        ]

        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)

    def test_cannot_create_review_with_invalid_stars(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json")
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json")

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # trying to create review with invalid number of stars
        response = client.post(
            "/api/movies/1/review/", self.wrong_review_data, format="json"
        )
        self.assertEqual(response.status_code, 400)

        # verifying if criticism is nested with movie
        response = client.get("/api/movies/1/").json()

        self.assertEqual(len(response["reviews"]), 0)

    def test_update_review_that_doesnt_exist(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user trying to update review that doesnt exists
        response = client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_update_review_from_unexisting_movie(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()
        # create regular user
        client.post("/api/accounts/", self.user_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user trying to update review when movie doesnt exists
        response = client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_critic_can_update_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")
        client.post("/api/movies/", self.movie_data_2, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user creating review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        # critic user trying to update review
        response = client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        expected_review_response = {
            "id": 1,
            "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
            "stars": 10,
            "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
            "spoilers": True,
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_review_response)

        # verifying if uppdated criticism is nested with movie correctly
        response = client.get("/api/movies/1/").json()
        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 10,
                "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
                "spoilers": True,
            }
        ]
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)

    def test_user_cannot_update_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()
        # create regular user
        client.post("/api/accounts/", self.user_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user creating review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        # login with regular user
        token = client.post("/api/login/", self.user_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # regular user trying to update critic review
        response = client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 403)

        # verifying if uppdated criticism is nested with movie correctly
        response = client.get("/api/movies/1/").json()
        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 2,
                "review": "Muito fraco",
                "spoilers": False,
            }
        ]
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)

    def test_admin_cannot_update_review(self):
        client = APIClient()

        # create admin user
        client.post("/api/accounts/", self.admin_data, format="json").json()
        # create critc user
        client.post("/api/accounts/", self.critic_data, format="json").json()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # creating movies to receive reviews
        client.post("/api/movies/", self.movie_data_1, format="json")

        # login with critic user
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # critic user creating review
        response = client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        # login with admin
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # admin trying to update critic review
        response = client.put(
            "/api/movies/1/review/", self.review_data_2, format="json"
        )
        self.assertEqual(response.status_code, 403)

        # verifying if uppdated criticism is nested with movie correctly
        response = client.get("/api/movies/1/").json()
        expected_reviews = [
            {
                "id": 1,
                "critic": {"id": 2, "first_name": "John", "last_name": "Doe"},
                "stars": 2,
                "review": "Muito fraco",
                "spoilers": False,
            }
        ]
        self.assertEqual(len(response["reviews"]), 1)
        self.assertEqual(response["reviews"], expected_reviews)


class TestListReview(APITestCase):
    def setUp(self):
        user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": False,
            "is_staff": False,
        }

        self.user = self.client.post("/api/accounts/", data=user_data, format="json")

        self.user_login_data = {
            "username": "user",
            "password": "1234",
        }

        critic_data = {
            "username": "critic",
            "password": "1234",
            "first_name": "Bruce",
            "last_name": "Wayne",
            "is_superuser": False,
            "is_staff": True,
        }

        self.critic = self.client.post("/api/accounts/", critic_data, format="json")

        self.critic_login_data = {
            "username": "critic",
            "password": "1234",
        }

        critic_data_2 = {
            "username": "critic2",
            "password": "1234",
            "first_name": "Clark",
            "last_name": "Kent",
            "is_superuser": False,
            "is_staff": True,
        }

        self.critic2 = self.client.post("/api/accounts/", critic_data_2, format="json")

        self.critic_login_data_2 = {
            "username": "critic2",
            "password": "1234",
        }

        admin_data = {
            "username": "admin",
            "password": "1234",
            "first_name": "John",
            "last_name": "Doe",
            "is_superuser": True,
            "is_staff": True,
        }

        self.admin = self.client.post("/api/accounts/", admin_data, format="json")

        self.admin_login_data = {
            "username": "admin",
            "password": "1234",
        }

        self.movie_data = {
            "title": "O Poderoso Chefão",
            "duration": "175m",
            "genres": [{"name": "Crime"}, {"name": "Drama"}],
            "premiere": "1972-09-10",
            "classification": 14,
            "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' de Nova York que está feliz, pois Connie (Talia Shire), sua filha,se casou com Carlo (Gianni Russo). Por ser seu padrinho Vito foi procurar o líder da banda e ofereceu 10 mil dólares para deixar Johnny sair, mas teve o pedido recusado.",
        }

        self.review_data_1 = {
            "stars": 2,
            "review": "Muito fraco",
            "spoilers": False,
        }

        self.review_data_2 = {
            "stars": 10,
            "review": "Ótimo filme. Adorei a parte em que o fulaninho resgatou a fulaninha",
            "spoilers": True,
        }

        # login
        token = self.client.post(
            "/api/login/", self.admin_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create movie
        movie = self.client.post("/api/movies/", self.movie_data, format="json")

        token = self.client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.post(
            "/api/movies/1/review/", self.review_data_1, format="json"
        )

        token = self.client.post(
            "/api/login/", self.critic_login_data_2, format="json"
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.client.post("/api/movies/1/review/", self.review_data_2, format="json")

    def test_anonymous_cannot_view_reviews(self):
        client = APIClient()

        response = client.get("/api/reviews/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {"detail": "Authentication credentials were not provided."},
        )

    def test_user_cannot_view_reviews(self):
        client = APIClient()

        # login with admin user for create movies
        token = client.post("/api/login/", self.user_login_data, format="json").json()[
            "token"
        ]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = client.get("/api/reviews/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You do not have permission to perform this action."},
        )

    def test_critic_can_view_only_own_reviews(self):
        client = APIClient()

        # login with admin user for create movies
        token = client.post(
            "/api/login/", self.critic_login_data, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = client.get("/api/reviews/")

        review_1 = {
            "id": 1,
            "stars": 2,
            "review": "Podia ser muito melhor",
            "spoilers": False,
        }

        critic_1 = {"first_name": "Bruce", "last_name": "Wayne"}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertDictContainsSubset(self.review_data_1, response.json()[0])
        self.assertDictContainsSubset(critic_1, response.json()[0]["critic"])

        review_2 = {
            "id": 2,
            "stars": 10,
            "review": "Melhor filme que ja assisti",
            "spoilers": True,
        }

        critic_2 = {"first_name": "Clark", "last_name": "Kent"}

        token = client.post(
            "/api/login/", self.critic_login_data_2, format="json"
        ).json()["token"]
        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertDictContainsSubset(self.review_data_2, response.json()[0])
        self.assertDictContainsSubset(critic_2, response.json()[0]["critic"])

    def test_admin_can_view_all_reviews(self):
        client = APIClient()

        # login with admin user for create movies
        token = client.post("/api/login/", self.admin_login_data, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = client.get("/api/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

        critic_1 = {"first_name": "Bruce", "last_name": "Wayne"}

        self.assertDictContainsSubset(critic_1, response.json()[0]["critic"])

        critic_2 = {"first_name": "Clark", "last_name": "Kent"}

        self.assertDictContainsSubset(critic_2, response.json()[1]["critic"])
