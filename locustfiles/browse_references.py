from random import choice
from locust import HttpUser, task, between

from references.models import Reference


class BrowseReferences(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.REFERENCES_UUIDS = list(Reference.objects.all().values_list("uuid", flat=True))

    @task(weight=1)
    def view_references(self):
        self.client.get(
            f"/references/",
            name="/references",
        )

    @task(weight=2)
    def view_reference(self):
        self.client.get(
            f"/references/{choice(self.REFERENCES_UUIDS)}",
            name="/references/:uuid",
        )
