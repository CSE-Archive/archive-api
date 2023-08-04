from rest_framework.routers import SimpleRouter

from recordings.views import RecordedClassroomViewSet


router = SimpleRouter()
router.register("recordings", RecordedClassroomViewSet, basename="recordings")

urlpatterns = router.urls
