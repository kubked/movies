from rest_framework import routers

from api.views import MovieViewSet

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
urlpatterns = router.urls
