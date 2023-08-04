from rest_framework.routers import SimpleRouter

from professors.views import ProfessorViewSet


router = SimpleRouter()
router.register("professors", ProfessorViewSet, basename="professors")

urlpatterns = router.urls
