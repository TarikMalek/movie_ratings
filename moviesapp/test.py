from django.test import TestCase,Client
from rest_framework.test import APIClient
from rest_framework import status
from serializers.MovieSerializer import MovieSerializer
from moviesapp.models import Movie,Rating
from django.urls import reverse
import json


client = Client()


class MovieModelTagTest(TestCase):
  
    def test_tag_model_str(self):
        movie = Movie.objects.create(
            title = "Test Movie Creation"
        )
  
        self.assertEqual(str(movie), movie.title)

class GetAllMoviesTest(TestCase):
    """ Test module for GET all movies API """

    def setUp(self):
        Movie.objects.create(
            title='Movie1'
        )
        Movie.objects.create(
            title='Movie2'
        )
        Movie.objects.create(
            title='Movie3'
        )
        Movie.objects.create(
            title='Movie4'
        )

    def test_get_all_movies(self):
        # get API response
        response = client.get(reverse('post_movie'))
        # get data from db
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleMovieTest(TestCase):
    """ Test module for GET single movie API """

    def setUp(self):
        self.casper = Movie.objects.create(
            title='Casper'
        )
        self.crash = Movie.objects.create(
            title='Crash'
        )
        self.avatar = Movie.objects.create(
            title='Avatar'
        )
        

    def test_get_valid_single_movie(self):
        response = client.get(
            reverse('get_movie', kwargs={'id': self.casper.pk}))
        movie = Movie.objects.get(pk=self.casper.pk)
        serializer = MovieSerializer(movie)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_movie(self):
        response = client.get(
            reverse('get_movie', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewMovieTest(TestCase):
    """ Test module for inserting a new movie """

    def setUp(self):
        self.valid_payload = {
            'title': 'Muffin',
        }
        self.invalid_payload = {
            'title': '',
        }

    def test_create_valid_movie(self):
        response = client.post(
            reverse('post_movie'),
            data = json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_movie(self):
        response = client.post(
            reverse('post_movie'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNewRatingTest(TestCase):
    """ Test module for inserting a new rating """

    def setUp(self):
        Movie.objects.create(
            title='Movie1'
        )
        self.valid_payload = {
            'value': 5,
            'movie_id' : 1
        }
        self.invalid_movie_payload = {
            'value': 5,
            'movie_id' : 10
        }
        self.invalid_rating_payload = {
            'value': 6,
            'movie_id' : 1
        }
    
    def test_create_valid_rating(self):
        response = client.post(
            reverse('create_rating'),
            data = json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_create_invalid_rating(self):
        response = client.post(
            reverse('create_rating'),
            data=json.dumps(self.invalid_rating_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_create_invalid_movie_id(self):
        response = client.post(
            reverse('create_rating'),
            data=json.dumps(self.invalid_movie_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 