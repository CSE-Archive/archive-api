from pytest import mark
from model_bakery import baker

from rest_framework import status

from courses.models import Resource


@mark.django_db
class TestRetriveResource:
    def test_if_resource_exists_returns_200(self, api_client):
        resource = baker.make(Resource)

        response = api_client.get(f"/resources/{resource.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == resource.id

    def test_if_resource_not_exists_returns_404(self, api_client):
        resources_ids = Resource.objects.all().values_list("id", flat=True)
        not_existing_resource_id = resources_ids[-1] if resources_ids else 1
        while not_existing_resource_id in resources_ids:
            not_existing_resource_id += 1

        response = api_client.get(f"/resources/{not_existing_resource_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListResource:
    def test_if_resources_exists_returns_200(self, api_client):
        resources = baker.make(Resource, _quantity=10)
        resources_ids = set(resource.id for resource in resources)

        response = api_client.get(f"/resources/")
        response_ids = set(resource["id"] for resource in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert resources_ids.issubset(response_ids)
