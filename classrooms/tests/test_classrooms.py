from pytest import mark
from model_bakery import baker

from rest_framework import status

from classrooms.models import Classroom


@mark.django_db
class TestRetrieveClassroom:
    def test_if_classroom_exists_returns_200(self, api_client):
        classroom = baker.make(Classroom)

        response = api_client.get(f"/classrooms/{classroom.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == classroom.id

    def test_if_classroom_not_exists_returns_404(self, api_client):
        classrooms_ids = Classroom.objects.all().values_list("id", flat=True)
        not_existing_classroom_id = classrooms_ids[-1] if classrooms_ids else 1
        while not_existing_classroom_id in classrooms_ids:
            not_existing_classroom_id += 1

        response = api_client.get(f"/classrooms/{not_existing_classroom_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListClassroom:
    def test_if_classrooms_exists_returns_200(self, api_client):
        classrooms = baker.make(Classroom, _quantity=10)
        classrooms_ids = set(classroom.id for classroom in classrooms)

        response = api_client.get(f"/classrooms/")
        response_ids = set(classroom["id"] for classroom in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert classrooms_ids.issubset(response_ids)
