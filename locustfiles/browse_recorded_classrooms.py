from random import choice
from locust import HttpUser, task, between

from classrooms.models import Classroom
from recordings.models import RecordedClassroom


class BrowseRecordedClassroom(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.CLASSROOM_UUID_CHOICES = list(Classroom.objects.all().values_list("uuid", flat=True))
        self.RECORDED_CLASSROOM_UUIDS = list(RecordedClassroom.objects.all().values_list("uuid", flat=True))

    @task(weight=1)
    def view_recordings(self):
        self.client.get(
            f"/recordings/?classroom={choice(self.CLASSROOM_UUID_CHOICES)}",
            name="/recordings",
        )

    @task(weight=2)
    def view_resource(self):
        self.client.get(
            f"/recordings/{choice(self.RECORDED_CLASSROOM_UUIDS)}",
            name="/recordings/:uuid",
        )
