from rest_framework.routers import SimpleRouter

from references.views import ReferenceViewSet


router = SimpleRouter()
router.register("references", ReferenceViewSet, basename="references")

urlpatterns = router.urls
