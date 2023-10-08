from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from movie_rating_platform.models import Movie, Rating


class MovieRatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.movie = Movie.objects.create(
            title="Test Movie", release_year=2022
        )
        self.client.login(username="testuser", password="testpassword")

    def test_movie_list_view(self):
        response = self.client.get(reverse("movie_rating:movie-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_movie_detail_view(self):
        response = self.client.get(
            reverse("movie_rating:movie-detail", args=[self.movie.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_create_rating_view(self):
        response = self.client.post(
            reverse("movie_rating:create-rating", args=[self.movie.pk]),
            {"value": 8, "description": "Great movie!"},
        )
        self.assertEqual(response.status_code, 302)
        rating = Rating.objects.get(movie=self.movie, sender=self.user)
        self.assertEqual(rating.value, 8)
        self.assertEqual(rating.description, "Great movie!")

    def test_toggle_assign_to_movie(self):
        response = self.client.get(
            reverse("movie_rating:toggle-assign", args=[self.movie.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.movie in self.user.visitor.wishlist.all())


class RegisterViewTests(TestCase):
    def test_register_view(self):
        test_username = "testuser"
        test_password = "testpassword"
        test_email = "test@example.com"
        response = self.client.post(
            reverse("register"),
            {
                "username": test_username,
                "password": test_password,
                "email": test_email,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register_done.html")
        self.assertTrue(User.objects.filter(username=test_username).exists())
        login_response = self.client.login(
            username=test_username, password=test_password
        )
        self.assertTrue(login_response)
