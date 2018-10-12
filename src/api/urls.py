from django.conf.urls import url
from rest_framework import routers

from api.views import CommentsViewSet, MovieViewSet, TopMovies


# register viewsets
router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
# CommentsViewSet doesn't have default queryset and needs to define base_name
router.register(r'comments', CommentsViewSet, base_name='comment')

urlpatterns = [
    url(r'^top$', TopMovies.as_view(), name='top')
]

urlpatterns += router.urls
