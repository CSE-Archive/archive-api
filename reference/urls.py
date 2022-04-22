from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register("references", views.ReferenceViewSet)


urlpatterns = router.urls
