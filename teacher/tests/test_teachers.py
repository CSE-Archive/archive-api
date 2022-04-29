from pytest import mark
from model_bakery import baker
from rest_framework import status
from teacher.models import Teacher


@mark.django_db
class TestRetriveTeacher:
    def test_if_teacher_exists_returns_200(self, api_client):
        teacher = baker.make(Teacher)

        response = api_client.get(f"/teachers/{teacher.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == teacher.id

    def test_if_teacher_not_exists_returns_404(self, api_client):
        teachers_ids = Teacher.objects.all().values_list("id", flat=True)
        not_existing_teacher_id = teachers_ids[-1] if teachers_ids else 1
        while not_existing_teacher_id in teachers_ids:
            not_existing_teacher_id += 1

        response = api_client.get(f"/teachers/{not_existing_teacher_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListTeacher:
    def test_if_teachers_exists_returns_200(self, api_client):
        teachers = baker.make(Teacher, _quantity=10)
        teachers_ids = set(teacher.id for teacher in teachers)

        response = api_client.get(f"/teachers/")
        response_ids = set(teacher["id"] for teacher in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert teachers_ids.issubset(response_ids)
