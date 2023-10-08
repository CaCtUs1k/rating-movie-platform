from django.test import TestCase
from movie_rating_platform.forms import (
    AvatarForm,
    MovieSearchForm,
    VisitorSearchForm,
    VisitorCreationForm,
    VisitorUpdateForm,
    CreateOrUpdateRatingForm,
)


class AvatarFormTests(TestCase):
    def test_avatar_form(self):
        form_data = {
            "avatar": "path/to/avatar.jpg",
        }
        form = AvatarForm(data=form_data)

        self.assertTrue(form.is_valid())


class MovieSearchFormTests(TestCase):
    def test_movie_search_form(self):
        form_data = {
            "title": "Test Movie",
        }
        form = MovieSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class VisitorSearchFormTests(TestCase):
    def test_visitor_search_form(self):
        form_data = {
            "username": "testuser",
        }
        form = VisitorSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class VisitorCreationFormTests(TestCase):
    def test_visitor_creation_form(self):
        form_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = VisitorCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_visitor_creation_form_password_mismatch(self):
        form_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "mismatchedpassword",
        }
        form = VisitorCreationForm(data=form_data)

        self.assertFalse(form.is_valid())


class VisitorUpdateFormTests(TestCase):
    def test_visitor_update_form(self):
        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "username": "testuser",
            "email": "updated@example.com",
        }
        form = VisitorUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())


class CreateOrUpdateRatingFormTests(TestCase):
    def test_create_or_update_rating_form(self):
        form_data = {
            "value": 8,
            "description": "Great movie!",
        }
        form = CreateOrUpdateRatingForm(data=form_data)

        self.assertTrue(form.is_valid())
