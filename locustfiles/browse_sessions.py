from random import choice
from locust import HttpUser, task, between
from course.models import Course, Session


class BrowseSessions(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.COURSE_ID_CHOICES = list(Course.objects.all().values_list("id", flat=True))
        self.SESSIONS_IDS = list(Session.objects.all().values_list("id", flat=True))

    @task(weight=1)
    def view_sessions(self):
        self.client.get(
            f"/sessions/?course_id={choice(self.COURSE_ID_CHOICES)}",
            name="/sessions",
        )

    @task(weight=2)
    def view_session(self):
        self.client.get(
            f"/sessions/{choice(self.SESSIONS_IDS)}",
            name="/sessions/:id",
        )
