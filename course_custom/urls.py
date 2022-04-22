from . import views
from course.urls import router, courses_router
from rest_framework_nested import routers

courses_router.register("references", views.ReferenceItemViewSet, basename="courses-references")

sessions_router = routers.NestedDefaultRouter(router, "sessions", lookup="session")
sessions_router.register("teachers", views.TeacherItemViewSet, basename="sessions-teachers")

urlpatterns = courses_router.urls + sessions_router.urls
