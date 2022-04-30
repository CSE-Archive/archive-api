from random import choice
from locust import HttpUser, task, between
from teacher.models import Teacher


class BrowseTeachers(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.TEACHERS_IDS = list(Teacher.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_teachers(self):
        self.client.get(
            f"/teachers/",
            name="/teachers",
        )

    @task(weight=2)
    def view_teacher(self):
        self.client.get(
            f"/teachers/{choice(self.TEACHERS_IDS)}",
            name="/teachers/:id",
        )
