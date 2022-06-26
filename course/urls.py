from .views import CourseViewSet, ClassroomViewSet, ResourceViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("courses", CourseViewSet, basename="courses")
router.register("classrooms", ClassroomViewSet, basename="classrooms")
router.register("resources", ResourceViewSet)

urlpatterns = router.urls
