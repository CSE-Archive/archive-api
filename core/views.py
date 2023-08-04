from rest_framework.views import APIView
from rest_framework.response import Response

from courses.views import CourseViewSet
from resources.views import ResourceViewSet
from references.views import ReferenceViewSet
from professors.views import ProfessorViewSet
from recordings.views import RecordedClassroomViewSet


class MultilpeView(APIView):
    viewset_classes = []

    def get(self, request):
        data = {
            viewset_data["name"]: viewset_data["viewset"].as_view({"get": "list"})(request._request).data
            for viewset_data in self.viewset_classes
        }
        return Response(data)


class HomeView(MultilpeView):
    viewset_classes = [
        {"name": "resources", "viewset": ResourceViewSet},
        {"name": "references", "viewset": ReferenceViewSet},
        {"name": "recordings", "viewset": RecordedClassroomViewSet},
    ]


class SearchView(MultilpeView):
    viewset_classes = [
        {"name": "courses", "viewset": CourseViewSet},
        {"name": "resources", "viewset": ResourceViewSet},
        {"name": "references", "viewset": ReferenceViewSet},
        {"name": "professors", "viewset": ProfessorViewSet},
        {"name": "recordings", "viewset": RecordedClassroomViewSet},
    ]
