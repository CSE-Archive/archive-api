from rest_framework.routers import SimpleRouter

from classrooms.views import ClassroomViewSet


router = SimpleRouter()
router.register("classrooms", ClassroomViewSet, basename="classrooms")

urlpatterns = router.urls
