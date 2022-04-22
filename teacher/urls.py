from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register("teachers", views.TeacherViewSet)


urlpatterns = router.urls
