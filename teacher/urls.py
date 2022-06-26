from .views import TeacherViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("teachers", TeacherViewSet)


urlpatterns = router.urls
