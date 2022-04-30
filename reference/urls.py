from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("references", views.ReferenceViewSet)


urlpatterns = router.urls
