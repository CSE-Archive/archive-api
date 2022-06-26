from random import choice
from locust import HttpUser, task, between
from course.models import Course, Classroom


class BrowseClassrooms(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.COURSE_ID_CHOICES = list(Course.objects.all().values_list("id", flat=True))
        self.CLASSROOMS_IDS = list(Classroom.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_classrooms(self):
        self.client.get(
            f"/classrooms/?course_id={choice(self.COURSE_ID_CHOICES)}",
            name="/classrooms",
        )

    @task(weight=2)
    def view_classroom(self):
        self.client.get(
            f"/classrooms/{choice(self.CLASSROOMS_IDS)}",
            name="/classrooms/:id",
        )
