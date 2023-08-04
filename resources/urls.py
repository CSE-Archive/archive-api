from rest_framework.routers import SimpleRouter

from resources.views import ResourceViewSet


router = SimpleRouter()
router.register("resources", ResourceViewSet, basename="resources")

urlpatterns = router.urls
