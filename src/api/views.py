import datetime
import logging

from django.utils.text import slugify
from django.db import IntegrityError
from django.db.models import Case, F, Sum, When
from django.db.models.expressions import Window
from django.db.models.fields import IntegerField
from django.db.models.functions import DenseRank, Coalesce
from django.shortcuts import get_object_or_404
from requests.exceptions import HTTPError, RequestException
from rest_framework import exceptions, mixins, status, viewsets, views
from rest_framework.response import Response

from api.models import Comment, Movie
from api.serializers import CommentSerializer
from api.serializers import MovieSerializer, MovieRequestSerializer
from api.services import get_omdb_movie


logger = logging.getLogger(__name__)


class MovieViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """View set providing handlers for POST and GET on /movies"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        """Create movie entry based on sent title. Handle POST on /movies

        This method calls `get_omdb_movie` which requests external API.
        """
        movie_request = MovieRequestSerializer(data=request.data)

        def movie_exists_response():
            return Response({
                'title': ['Movie with given title already exists.']
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
            logging.error('omdabpi http error: %s - %r', e.errno, e.strerror)
            return Response({
                'OMDB API': [
                    e.strerror,
                ],
            })
        except RequestException as e:
            logging.error('omdbapi raised exception: %r', e)
            return Response({
                'OMDB API': [
                    'External service is unavailable. Please try again later.',
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
        logger.info('Created new movie: %s', movie.title)
        # return new movie in response
        return Response(MovieSerializer(movie).data)


class CommentsViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """View set providing handlers for POST and GET on /comments"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Optionally filter to `movie_id` passed in querystring."""
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise exceptions.ValidationError({
                    'movie_id': [
                        'Incorrect movie_id type. Expected int.',
                    ],
                })
            movie = get_object_or_404(Movie, id=movie_id)
            queryset = queryset.filter(movie_id=movie)
        return queryset


class TopMovies(views.APIView):
    """View to list top movies in specified date range."""
    def get_start_end_date_from_request(self, request):
        """Validate start and end date."""
        missing_params = {}
        # get start and end date from query_params
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        if start is None:
            missing_params['start'] = [
                'Query parameter "start" not found.'
            ]
        if end is None:
            missing_params['end'] = [
                'Query parameter "end" not found.'
            ]
        if missing_params:
            raise exceptions.NotFound(missing_params)
        # check if they are valid dates
        invalid_date = {}
        date_format = '%Y-%m-%d'
        try:
            start_date = datetime.datetime.strptime(start, date_format)
        except ValueError:
            invalid_date['start'] = [
                'Query parameter "start" is not in YYYY-MM-DD format.'
            ]
        try:
            end_date = datetime.datetime.strptime(end, date_format)
            # add one day to the end range to include comments from end day
            end_date += datetime.timedelta(days=1)
            end = end_date.strftime(date_format)
        except ValueError:
            invalid_date['end'] = [
                'Query parameter "end" is not in YYYY-MM-DD format.'
            ]
        if invalid_date:
            raise exceptions.ValidationError(invalid_date)

        if end_date < start_date:
            raise exceptions.ValidationError({
                'start': [
                    'start date should be less than or equal end date'
                ]
            })
        return start, end

    def get(self, request):
        """Extract dates range from query_params and return top movies."""
        start, end = self.get_start_end_date_from_request(request)
        # pull ranked movies sorted by number of comments in given date range
        movies_query = Movie.objects.annotate(
            total_comments=Coalesce(
                Sum(Case(
                    When(comment__created__range=[start, end], then=1),
                    output_field=IntegerField()
                )),
                0
            ),
            rank=Window(
                expression=DenseRank(),
                order_by=F('total_comments').desc(),
            )
        ).order_by('-total_comments', 'id')
        # extract needed fields to response
        # it's too trivial to use Serializer here
        movies = [
            {
                'movie_id': movie.id,
                'total_comments': movie.total_comments,
                'rank': movie.rank
            } for movie in movies_query
        ]
        return Response(movies)