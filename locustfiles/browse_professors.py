from random import choice
from locust import HttpUser, task, between

from professors.models import Professor


class BrowseProfessors(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.PROFESSORS_UUIDS = list(Professor.objects.all().values_list("uuid", flat=True))

    @task(weight=1)
    def view_professors(self):
        self.client.get(
            f"/professors/",
            name="/professors",
        )

    @task(weight=2)
    def view_professor(self):
        self.client.get(
            f"/professors/{choice(self.PROFESSORS_UUIDS)}",
            name="/professors/:uuid",
        )
