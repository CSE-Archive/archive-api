from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register("courses", views.CourseViewSet)
router.register("sessions", views.SessionViewSet)
router.register("resources", views.ResourceViewSet)

courses_router = routers.NestedDefaultRouter(router, "courses", lookup="course")
courses_router.register("requisites", views.RequisitesViewSet, basename="courses-requisites")

urlpatterns = router.urls + courses_router.urls
