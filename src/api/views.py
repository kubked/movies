import logging

from django.utils.text import slugify
from django.db import IntegrityError
from requests.exceptions import HTTPError, RequestException
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from api.models import Movie
from api.serializers import MovieSerializer, MovieRequestSerializer
from api.services import get_omdb_movie


logger = logging.getLogger(__name__)


class MovieList(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        """Create movie entry based on sent title."""
        movie_request = MovieRequestSerializer(data=request.data)

        def movie_exists_response():
            return Response({
                "title": ["Movie with given title already exists."]
            }, status=status.HTTP_409_CONFLICT)

        if not movie_request.is_valid():
            return Response(
                movie_request.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # get title from request
        title = movie_request.validated_data['title']
        # slugify title and try to validate it's existence
        if Movie.objects.filter(slug=slugify(title)).exists():
            return movie_exists_response()

        # try to get movie from omdbapi and notify if it's not possible
        try:
            details = get_omdb_movie(title)
        except HTTPError as e:
            logging.error("omdabpi http error: %s - %r", e.errno, e.strerror)
            return Response({
                "OMDB API": [
                    e.strerror,
                ],
            })
        except RequestException as e:
            logging.error("omdbapi raised exception: %r", e)
            return Response({
                "OMDB API": [
                    "External service is unavailable. Please try again later.",
                ],
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        title = details['Title']
        movie = Movie(title=title, details=details, slug=slugify(title))
        # it should throw error when slugified title exists in database
        # and couldn't be verfied earlier (eg. incomplete title)
        try:
            movie.save()
        except IntegrityError:
            return movie_exists_response()
        logger.info("Created new movie: %s", movie.title)
        # return new movie in response
        return Response(MovieSerializer(movie).data)
