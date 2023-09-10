from rest_framework.routers import SimpleRouter

from professors.views import DepartmentViewSet ,ProfessorViewSet


router = SimpleRouter()
router.register("professors", ProfessorViewSet, basename="professors")
router.register("departments", DepartmentViewSet, basename="departments")

urlpatterns = router.urls
