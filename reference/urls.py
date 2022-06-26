from .views import ReferenceViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("references", ReferenceViewSet)


urlpatterns = router.urls
