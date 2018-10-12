import urllib.parse as urlparse

import requests

from core import settings


class InvalidStatusError(requests.exceptions.RequestException):
    """Server didn't send response with status code 200"""


def get_omdb_movie(movie_title):
    """Get movie details from external omdbapi.

    :raise requests.exceptions.RequestException: OMDB API call failed

    :param movie_title: unescaped movie title
    :return: JSON with movie details
    """
    params = {
        'apikey': settings.OMDB_API_KEY,
        't': movie_title,
    }
    response = requests.get(
        settings.OMDB_API_URL,
        params=params,
        timeout=settings.OMDB_API_TIMEOUT,
    )
    if response.ok:
        return response.json()
    else:
        raise InvalidStatusError()
