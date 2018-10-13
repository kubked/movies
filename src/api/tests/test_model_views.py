from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils.text import slugify
from rest_framework.test import APITestCase
from rest_framework import status

from api.models import Movie, Comment


class CommentsViewSetListTestCase(APITestCase):
    """Test retrieving comments list"""
    def setUp(self):
        def create_dummy_movie(title):
            return Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )

        self.movie1 = create_dummy_movie('First Movie')
        self.movie2 = create_dummy_movie('Second Movie')
        Comment.objects.create(movie_id=self.movie2, comment="comment 1")
        Comment.objects.create(movie_id=self.movie1, comment="comment 2")
        Comment.objects.create(movie_id=self.movie1, comment="comment 3")
        Comment.objects.create(movie_id=self.movie2, comment="comment 4")
        Comment.objects.create(movie_id=self.movie1, comment="comment 5")

        # get any movie id which for sure doesn't exist in db
        self.unexisting_movie_id = [
            x for x in [1, 2, 3] if x not in (self.movie1.id, self.movie2.id)
        ][0]

    def test_get_comments(self):
        """Test fetching list of all comments"""
        url = reverse('comment-list')
        response = self.client.get(url)
        payload = response.json()
        self.assertListEqual(
            sorted([comment['comment'] for comment in payload]),
            ['comment 1', 'comment 2', 'comment 3', 'comment 4', 'comment 5']
        )

    def test_get_comments_for_specified_movie(self):
        """Test fetching comments only for movie with specified id"""
        url = reverse('comment-list')
        response = self.client.get(url, {'movie_id': self.movie1.id})
        payload = response.json()
        self.assertListEqual(
            sorted([comment['comment'] for comment in payload]),
            ['comment 2', 'comment 3', 'comment 5']
        )

    def test_get_comments_for_unexisting_movie(self):
        url = reverse('comment-list')
        data = {'movie_id': self.unexisting_movie_id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_incorrect_movie_id_type(self):
        url = reverse('comment-list')
        data = {'movie_id': 'abcd'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentsViewSetCreateTestCase(APITestCase):
    """Test retrieving comments list"""
    def setUp(self):
        def create_dummy_movie(title):
            return Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )

        self.movie1 = create_dummy_movie('First Movie')
        self.movie2 = create_dummy_movie('Second Movie')
        Comment.objects.create(movie_id=self.movie2, comment="comment 1")
        Comment.objects.create(movie_id=self.movie1, comment="comment 2")
        Comment.objects.create(movie_id=self.movie1, comment="comment 3")
        Comment.objects.create(movie_id=self.movie2, comment="comment 4")
        Comment.objects.create(movie_id=self.movie1, comment="comment 5")

        # get any movie id which for sure doesn't exist in db
        self.unexisting_movie_id = [
            x for x in [1, 2, 3] if x not in (self.movie1.id, self.movie2.id)
        ][0]

    def test_comment_unexisting_movie(self):
        """Test creating comment to unexisting movie"""
        url = reverse('comment-list')
        data = {
            'comment': 'comment 6',
            'movie_id': self.unexisting_movie_id,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        # check if wrong comment is not in list
        response = self.client.get(url)
        payload = response.json()
        self.assertFalse(
            any(comment['comment'] == 'comment 6' for comment in payload)
        )

    def test_create_comment(self):
        """Test creating valid simple comment"""
        url = reverse('comment-list')
        data = {
            'comment': 'comment 7',
            'movie_id': self.movie1.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        payload = response.json()
        self.assertEqual(payload['comment'], data['comment'])
        self.assertEqual(payload['movie_id'], data['movie_id'])
        self.assertTrue('id' in payload)

    def test_create_utf8_comment(self):
        """Test creating comment containing utf8 chars"""
        url = reverse('comment-list')
        data = {
            'comment': '文字',
            'movie_id': self.movie1.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        payload = response.json()
        self.assertEqual(payload['comment'], data['comment'])

    def test_create_empty_comment(self):
        """Test creating comment with empty text"""
        url = reverse('comment-list')
        data = {
            'comment': '',
            'movie_id': self.movie1.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_comment_without_movie(self):
        """Test creating comment with missing `movie_id`"""
        url = reverse('comment-list')
        data = {
            'comment': 'comment 8',
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )


class MovieViewSetCreateTestCase(APITestCase):
    """Test set focused on creating new movie's entries"""
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
        response = self.client.post(url, data)
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
        response = self.client.post(url, data)
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
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), movies_before_request + 1)

    def test_create_without_title(self):
        """Check title presence validation"""
        url = reverse('movie-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_too_long_title(self):
        """Try to create movie with too long title (>255 chars)"""
        url = reverse('movie-list')
        response = self.client.post(url, {'title': 'AB' * 150})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_empty_title(self):
        """Try to create movie with empty title"""
        url = reverse('movie-list')
        response = self.client.post(url, {'title': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_wrong_content_type(self):
        """Try to create movie with another content_type than JSON"""
        url = reverse('movie-list')
        response = self.client.post(
            url, {'title': 'ABC'}, content_type='application/octet-stream'
        )
        self.assertEqual(
            response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )


class MovieViewSetListCreateTestCase(APITestCase):
    """Test set focused on retrieving movies using API after movie creation"""
    def setUp(self):
        def create_dummy_movie(title):
            Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )
        create_dummy_movie('First Movie')
        create_dummy_movie('Second Movie')

    @patch('api.services.requests.get')
    def test_create_movie_and_get_movies_list(self, mock):
        """Create new movie and check if it's on list"""
        movie = {
            'Title': 'Third Movie',
            'Response': 'True',
        }
        mock.return_value = Mock(ok=True)
        mock.return_value.json.return_value = movie

        url = reverse('movie-list')

        # get old list
        response = self.client.get(url)
        payload = response.json()
        self.assertEqual(len(payload), 2)

        # create new movie
        self.client.post(url, {'title': 'Third Movie'})

        # get updated list
        response = self.client.get(url)
        payload = response.json()
        self.assertEqual(len(payload), 3)
        # check if new movie is on list
        self.assertTrue(
            any(movie['title'] == 'Third Movie' for movie in payload)
        )


class MovieViewSetListTestCase(APITestCase):
    """Test set focused on retrieving movies using API"""
    def setUp(self):
        def create_dummy_movie(title):
            Movie.objects.create(
                title=title,
                details={'Title': title},
                slug=slugify(title)
            )
        create_dummy_movie('First Movie')
        create_dummy_movie('Second Movie')

    def test_get_movies_list(self):
        """Get list of all movies in DB"""
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)
        # check if all details are not empty
        self.assertTrue(all(movie['details'] for movie in payload))
