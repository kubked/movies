from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils.text import slugify
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Movie


class MovieViewSetTestCase(APITestCase):
    def setUp(self):
        def create_dummy_movie(title):
            Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )
        create_dummy_movie('First Movie')
        create_dummy_movie('Second Movie')

    def test_create_existing_movie(self):
        """Try to create movie which exists in database."""
        url = reverse('movie-list')
        data = {'title': 'First Movie'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch('api.services.requests.get')
    def test_create_existing_movie_with_incomplete_title(self, mock):
        """Try to create movie which exists in database with full title"""
        movie = {
            'Title': 'Second Movie',
            'Response': 'True',
        }
        mock.return_value = Mock(ok=True)
        mock.return_value.json.return_value = movie

        url = reverse('movie-list')
        data = {'title': 'second'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    @patch('api.services.requests.get')
    def test_create_new_movie(self, mock):
        """Test creating completely new movie"""
        movies_before_request = Movie.objects.count()

        movie = {
            'Title': 'Third Movie',
            'Response': 'True',
        }
        mock.return_value = Mock(ok=True)
        mock.return_value.json.return_value = movie

        url = reverse('movie-list')
        data = {'title': 'Third Movie'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), movies_before_request + 1)

    def test_create_without_title(self):
        """Check title presence validation"""
        url = reverse('movie-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wrong_content_type(self):
        """Try to create movie with another content_type than JSON"""
        url = reverse('movie-list')
        response = self.client.post(
            url, {'title': 'ABC'}, content_type='application/octet-stream'
        )
        self.assertEqual(
            response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )