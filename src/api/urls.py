from rest_framework import routers

from api.views import CommentsViewSet, MovieViewSet

# register viewsets
router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
# CommentsViewSet doesn't have default queryset and needs to define base_name
router.register(r'comments', CommentsViewSet, base_name='comment')

urlpatterns = router.urls
