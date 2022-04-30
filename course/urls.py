from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("courses", views.CourseViewSet, basename="courses")
router.register("sessions", views.SessionViewSet, basename="sessions")
router.register("resources", views.ResourceViewSet)

urlpatterns = router.urls
