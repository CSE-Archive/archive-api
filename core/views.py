from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response

from courses.views import CourseViewSet
from resources.views import ResourceViewSet
from references.views import ReferenceViewSet
from professors.views import ProfessorViewSet
from recordings.views import RecordedClassroomViewSet


class MultilpeView(APIView):
    default_pagination_params = []
    viewset_classes = []

    def get(self, request):
        request._request.GET._mutable = True
        for param in self.default_pagination_params:
            request._request.GET[param[0]] = param[1]
        request._request.GET._mutable = False

        data = {
            viewset_data["name"]: viewset_data["viewset"].as_view({"get": "list"})(request._request).data.get("results")
            for viewset_data in self.viewset_classes
        }
        return Response(data)


class HomeView(MultilpeView):
    default_pagination_params = [
        ("limit", "10"),
        ("offset", "0"),
    ]
    viewset_classes = [
        {"name": "resources", "viewset": ResourceViewSet},
        {"name": "references", "viewset": ReferenceViewSet},
        {"name": "recordings", "viewset": RecordedClassroomViewSet},
    ]


class SearchView(MultilpeView):
    default_pagination_params = [
        ("limit", "10"),
        ("offset", "0"),
    ]
    viewset_classes = [
        {"name": "courses", "viewset": CourseViewSet},
        {"name": "resources", "viewset": ResourceViewSet},
        {"name": "references", "viewset": ReferenceViewSet},
        {"name": "professors", "viewset": ProfessorViewSet},
        {"name": "recordings", "viewset": RecordedClassroomViewSet},
    ]
