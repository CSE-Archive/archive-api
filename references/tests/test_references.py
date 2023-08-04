from pytest import mark
from model_bakery import baker

from rest_framework import status

from references.models import Reference


@mark.django_db
class TestRetriveReference:
    def test_if_reference_exists_returns_200(self, api_client):
        reference = baker.make(Reference)

        response = api_client.get(f"/references/{reference.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == reference.id

    def test_if_reference_not_exists_returns_404(self, api_client):
        references_ids = Reference.objects.all().values_list("id", flat=True)
        not_existing_reference_id = references_ids[-1] if references_ids else 1
        while not_existing_reference_id in references_ids:
            not_existing_reference_id += 1

        response = api_client.get(f"/references/{not_existing_reference_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListReference:
    def test_if_references_exists_returns_200(self, api_client):
        references = baker.make(Reference, _quantity=10)
        references_ids = set(reference.id for reference in references)

        response = api_client.get(f"/references/")
        response_ids = set(reference["id"] for reference in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert references_ids.issubset(response_ids)
