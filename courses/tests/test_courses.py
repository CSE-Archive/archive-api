from pytest import mark
from model_bakery import baker

from rest_framework import status

from courses.models import Course


@mark.django_db
class TestRetriveCourse:
    def test_if_course_exists_returns_200(self, api_client):
        course = baker.make(Course)

        response = api_client.get(f"/courses/{course.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == course.id

    def test_if_course_not_exists_returns_404(self, api_client):
        courses_ids = Course.objects.all().values_list("id", flat=True)
        not_existing_course_id = courses_ids[-1] if courses_ids else 1
        while not_existing_course_id in courses_ids:
            not_existing_course_id += 1

        response = api_client.get(f"/courses/{not_existing_course_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListCourse:
    def test_if_courses_exists_returns_200(self, api_client):
        courses = baker.make(Course, _quantity=10)
        courses_ids = set(course.id for course in courses)

        response = api_client.get(f"/courses/")
        response_ids = set(course["id"] for course in response.data)

        assert response.status_code == status.HTTP_200_OK
        assert courses_ids.issubset(response_ids)
