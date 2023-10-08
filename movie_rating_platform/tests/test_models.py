from django.test import TestCase
from movie_rating_platform.models import Genre, Movie, Visitor, Rating, Like


class GenreModelTest(TestCase):
    def test_genre_creation(self):
        genre = Genre.objects.create(name="Action")
        self.assertEqual(genre.name, "action")
        self.assertEqual(str(genre), "action")


class MovieModelTest(TestCase):
    def test_movie_creation(self):
        movie = Movie.objects.create(title="Inception", release_year=2010)
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.release_year, 2010)
        self.assertEqual(str(movie), "Inception (2010)")


class VisitorModelTest(TestCase):
    def test_visitor_creation(self):
        visitor = Visitor.objects.create(username="john_doe")
        self.assertEqual(visitor.username, "john_doe")
        self.assertEqual(str(visitor), "john_doe")


class RatingModelTest(TestCase):
    def test_rating_creation(self):
        visitor = Visitor.objects.create(username="john_doe")
        movie = Movie.objects.create(title="Inception", release_year=2010)
        rating = Rating.objects.create(value=8, sender=visitor, movie=movie)
        self.assertEqual(rating.value, 8)
        self.assertEqual(rating.sender, visitor)
        self.assertEqual(rating.movie, movie)
        self.assertIsNotNone(rating.create_time)
        self.assertEqual(str(rating), str(rating.description))


class LikeModelTest(TestCase):
    def test_like_creation(self):
        visitor = Visitor.objects.create(username="john_doe")
        movie = Movie.objects.create(title="Inception", release_year=2010)
        like = Like.objects.create(sender=visitor, target=movie)
        self.assertEqual(like.sender, visitor)
        self.assertEqual(like.target, movie)
