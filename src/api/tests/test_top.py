import datetime
import pytz
from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils.text import slugify
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Movie, Comment


class TopListTestCase(APITestCase):
    """Test retrieving movies top list"""
    def setUp(self):
        def create_dummy_movie(title):
            return Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )

        self.movie1 = create_dummy_movie('First Movie')
        self.movie2 = create_dummy_movie('Second Movie')
        mocked = datetime.datetime(2018, 4, 4, 1, 2, 3)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie2, comment="comment 1")
        mocked = datetime.datetime(2018, 4, 5, 10, 0, 0)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="comment 2")
        mocked = datetime.datetime(2018, 4, 6, 19, 0, 0)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="comment 3")
        mocked = datetime.datetime(2018, 4, 7, 12, 0, 0)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie2, comment="comment 4")
        mocked = datetime.datetime(2018, 4, 8, 3, 0, 0)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="comment 5")

    def test_top_all_comments(self):
        """Test fetching top with all comments"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2018-04-01',
            'end': '2018-04-09',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': self.movie1.id,
                    'total_comments': 3,
                    'rank': 1,
                },
                {
                    'movie_id': self.movie2.id,
                    'total_comments': 2,
                    'rank': 2,
                },
            ]
        )

    def test_top_one_day_comments(self):
        """Test fetching top with only selected one day"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2018-04-07',
            'end': '2018-04-07',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': self.movie2.id,
                    'total_comments': 1,
                    'rank': 1,
                },
                {
                    'movie_id': self.movie1.id,
                    'total_comments': 0,
                    'rank': 2,
                },
            ]
        )

    def test_empty_comments(self):
        """Test fetching top without any comments"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2018-01-07',
            'end': '2018-01-07',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': min(self.movie2.id, self.movie1.id),
                    'total_comments': 0,
                    'rank': 1,
                },
                {
                    'movie_id': max(self.movie2.id, self.movie1.id),
                    'total_comments': 0,
                    'rank': 1,
                },
            ]
        )

    def test_missing_start_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'end': '2018-01-07',
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_end_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2018-01-07',
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_both_params(self):
        url = reverse('top')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_start_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '9999-99-99',
            'end': '2018-01-07',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'end': 'ABCD',
            'start': '2018-01-07',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_after_end(self):
        url = reverse('top')
        response = self.client.get(url, {
            'end': '2018-01-01',
            'start': '2018-01-07',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_one_day_after_end(self):
        url = reverse('top')
        response = self.client.get(url, {
            'end': '2018-01-01',
            'start': '2018-01-02',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
