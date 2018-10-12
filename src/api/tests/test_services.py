from unittest.mock import Mock, patch

from requests.exceptions import RequestException
from nose.tools import assert_equal, assert_dict_equal, assert_raises
from django.test import TestCase

from api.services import get_omdb_movie


class OMDBAPITestCase(TestCase):
    @patch('api.services.requests.get')
    def test_omdb_api_getting_movie_succesfully(self, mock_omdb):
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
            "Plot": "This classic clip presents the story of a young girl ...",
            "Language": "English",
            "Country": "UK",
            "Awards": "N/A",
            "Poster": "https://images-na.ssl-images-amazon.com/images/MXVyNDE4OTY5NzI@._V1_SX300.jpg",
            "Ratings": [{"Source": "Internet Movie Database", "Value": "8.5/10"}],
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
        assert_dict_equal(response, movie)

    @patch('api.services.requests.get')
    def test_omdb_api_raising_exception(self, mock_omdb):
        mock_omdb.side_effect = RequestException()
        assert_raises(RequestException, get_omdb_movie, 'A-Ha!')

    def test_omdb_api_real_request(self):
        response = get_omdb_movie('A-Ha: Take on Me')
        assert_equal(response['Title'], 'A-Ha: Take on Me')
