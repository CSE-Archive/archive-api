from random import choice
from locust import HttpUser, task, between
from course.models import Session, Resource


class BrowseResources(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.SESSION_ID_CHOICES = list(Session.objects.all().values_list("id", flat=True))
        self.RESOURCES_IDS = list(Resource.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_resources(self):
        self.client.get(
            f"/resources/?session_id={choice(self.SESSION_ID_CHOICES)}",
            name="/resources",
        )

    @task(weight=2)
    def view_resource(self):
        self.client.get(
            f"/resources/{choice(self.RESOURCES_IDS)}",
            name="/resources/:id",
        )
