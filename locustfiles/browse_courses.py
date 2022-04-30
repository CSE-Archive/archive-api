from random import choice
from locust import HttpUser, task, between
from course.models import Course


class BrowseCourses(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.COURSES_IDS = list(Course.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_courses(self):
        self.client.get(
            f"/courses/",
            name="/courses",
        )

    @task(weight=2)
    def view_course(self):
        self.client.get(
            f"/courses/{choice(self.COURSES_IDS)}",
            name="/courses/:id",
        )
