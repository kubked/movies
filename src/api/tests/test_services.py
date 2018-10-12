from unittest.mock import Mock, patch

from requests.exceptions import RequestException
from django.test import TestCase

from api.services import get_omdb_movie


class OMDBAPITestCase(TestCase):
    """Test calling omdb api with movies database"""
    @patch('api.services.requests.get')
    def test_omdb_api_getting_movie_succesfully(self, mock_omdb):
        """Test getting sample movie with mocked request"""
        # set mock response
        movie = {
            "Title": "A-Ha: Take on Me",
            "Year": "1985",
            "Rated": "N/A",
            "Released": "N/A",
            "Runtime": "4 min",
            "Genre": "Short, Music",
            "Director": "Steve Barron",
            "Writer": "N/A",
            "Actors": "A-Ha, Bunty Bailey, Morten Harket, Philip Jackson",
            "Plot": "This classic clip presents the story of a young girl...",
            "Language": "English",
            "Country": "UK",
            "Awards": "N/A",
            "Poster": "https://images-na.ssl-images-amazon",
            "Ratings": [{"Source": "IMDB", "Value": "8.5/10"}],
            "Metascore": "N/A",
            "imdbRating": "8.5",
            "imdbVotes": "416",
            "imdbID": "tt4645418",
            "Type": "movie",
            "DVD": "N/A",
            "BoxOffice": "N/A",
            "Production": "N/A",
            "Website": "N/A",
            "Response": "True",
        }
        mock_omdb.return_value = Mock(ok=True)
        mock_omdb.return_value.json.return_value = movie

        response = get_omdb_movie("A-Ha: Take on Me")
        # compare get_omdb_move response with mocked movie
        self.assertDictEqual(response, movie)

    @patch('api.services.requests.get')
    def test_omdb_api_raising_exception(self, mock_omdb):
        """Test if exception is properly rethrowed or unhandled"""
        mock_omdb.side_effect = RequestException()
        with self.assertRaises(RequestException):
            get_omdb_movie('A-Ha!')

    def test_omdb_api_real_request(self):
        """Unmocked test with real api call"""
        response = get_omdb_movie('A-Ha: Take on Me')
        self.assertEqual(response['Title'], 'A-Ha: Take on Me')
