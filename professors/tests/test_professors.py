from pytest import mark
from model_bakery import baker
from rest_framework import status
from professors.models import Professor


@mark.django_db
class TestRetriveProfessor:
    def test_if_professor_exists_returns_200(self, api_client):
        professor = baker.make(Professor)

        response = api_client.get(f"/professors/{professor.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == professor.id

    def test_if_professor_not_exists_returns_404(self, api_client):
        professors_ids = Professor.objects.all().values_list("id", flat=True)
        not_existing_professor_id = professors_ids[-1] if professors_ids else 1
        while not_existing_professor_id in professors_ids:
            not_existing_professor_id += 1

        response = api_client.get(f"/professors/{not_existing_professor_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListProfessor:
    def test_if_professors_exists_returns_200(self, api_client):
        professors = baker.make(Professor, _quantity=10)
        professors_ids = set(professor.id for professor in professors)

        response = api_client.get(f"/professors/")
        response_ids = set(professor["id"] for professor in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert professors_ids.issubset(response_ids)
