from rest_framework import routers

from api.views import MovieList

router = routers.SimpleRouter()
router.register(r'movies', MovieList)
urlpatterns = router.urls
