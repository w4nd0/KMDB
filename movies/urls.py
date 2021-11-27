from rest_framework import routers

from movies.views import MovieView, ReviewView

router = routers.SimpleRouter()

router.register(r"movies", MovieView, basename="movies")
router.register(r"reviews", ReviewView, basename="reviews")

urlpatterns = router.urls
