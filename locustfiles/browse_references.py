from random import choice
from locust import HttpUser, task, between
from reference.models import Reference


class BrowseReferences(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.REFERENCES_IDS = list(Reference.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_references(self):
        self.client.get(
            f"/references/",
            name="/references",
        )

    @task(weight=2)
    def view_reference(self):
        self.client.get(
            f"/references/{choice(self.REFERENCES_IDS)}",
            name="/references/:id",
        )
