from random import choice
from locust import HttpUser, task, between

from courses.models import Course
from classrooms.models import Classroom


class BrowseClassrooms(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.COURSE_UUID_CHOICES = list(Course.objects.all().values_list("uuid", flat=True))
        self.CLASSROOMS_UUIDS = list(Classroom.objects.all().values_list("uuid", flat=True))

    @task(weight=1)
    def view_classrooms(self):
        self.client.get(
            f"/classrooms/?course={choice(self.COURSE_UUID_CHOICES)}",
            name="/classrooms",
        )

    @task(weight=2)
    def view_classroom(self):
        self.client.get(
            f"/classrooms/{choice(self.CLASSROOMS_UUIDS)}",
            name="/classrooms/:uuid",
        )
