from pytest import mark
from model_bakery import baker
from rest_framework import status
from course.models import Session


@mark.django_db
class TestRetriveSession:
    def test_if_session_exists_returns_200(self, api_client):
        session = baker.make(Session)

        response = api_client.get(f"/sessions/{session.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == session.id

    def test_if_session_not_exists_returns_404(self, api_client):
        sessions_ids = Session.objects.all().values_list("id", flat=True)
        not_existing_session_id = sessions_ids[-1] if sessions_ids else 1
        while not_existing_session_id in sessions_ids:
            not_existing_session_id += 1

        response = api_client.get(f"/sessions/{not_existing_session_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListSession:
    def test_if_sessions_exists_returns_200(self, api_client):
        sessions = baker.make(Session, _quantity=10)
        sessions_ids = set(session.id for session in sessions)

        response = api_client.get(f"/sessions/")
        response_ids = set(session["id"] for session in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert sessions_ids.issubset(response_ids)
