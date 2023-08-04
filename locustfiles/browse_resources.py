from random import choice
from locust import HttpUser, task, between

from classrooms.models import Classroom
from resources.models import Resource


class BrowseResources(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.CLASSROOM_UUID_CHOICES = list(Classroom.objects.all().values_list("uuid", flat=True))
        self.RESOURCES_UUIDS = list(Resource.objects.all().values_list("uuid", flat=True))

    @task(weight=1)
    def view_resources(self):
        self.client.get(
            f"/resources/?classroom={choice(self.CLASSROOM_UUID_CHOICES)}",
            name="/resources",
        )

    @task(weight=2)
    def view_resource(self):
        self.client.get(
            f"/resources/{choice(self.RESOURCES_UUIDS)}",
            name="/resources/:uuid",
        )
