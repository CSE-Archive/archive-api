from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("teachers", views.TeacherViewSet)


urlpatterns = router.urls
