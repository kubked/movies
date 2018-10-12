import logging

import requests

from core import settings


logger = logging.getLogger(__name__)


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
    response.raise_for_status()
    if response.ok:
        payload = response.json()
        # should be 404 IMO not 200 with 'Response': 'False'
        if payload['Response'] == 'False':
            raise requests.exceptions.HTTPError(404, 'Movie not found')
        else:
            logger.info("omdbapi request completed: %s", movie_title)
            return payload
    raise requests.exceptions.HTTPError(
        response.status_code, 'OMDB API exception'
    )
