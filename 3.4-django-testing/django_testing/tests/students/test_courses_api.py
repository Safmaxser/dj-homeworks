import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course_retrieve(client, student_factory, course_factory):
    students = student_factory(_quantity=2)
    course = course_factory(_quantity=1, students=students)
    rate_index = 0
    url = reverse('courses-detail', kwargs={"pk": course[rate_index].id})
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data['id'] == course[rate_index].id
    assert data['name'] == course[rate_index].name
    assert len(data['students']) == len(students)


@pytest.mark.django_db
def test_get_course_list(client, student_factory, course_factory):
    students = student_factory(_quantity=3)
    course = course_factory(_quantity=10, students=students)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    for index, item in enumerate(data):
        assert item['id'] == course[index].id
        assert item['name'] == course[index].name
        assert len(item['students']) == len(students)


@pytest.mark.django_db
def test_get_course_filter_id(client, student_factory, course_factory):
    students = student_factory(_quantity=5)
    course = course_factory(_quantity=10, students=students)
    rate_index = 2
    url = reverse('courses-list')
    url = f'{url}?id={course[rate_index].id}'
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course[rate_index].id
    assert data[0]['name'] == course[rate_index].name
    assert len(data[0]['students']) == len(students)


@pytest.mark.django_db
def test_get_course_filter_name(client, course_factory):
    course = course_factory(_quantity=10)
    rate_index = 3
    url = reverse('courses-list')
    url = f'{url}?name={course[rate_index].name}'
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == course[rate_index].id
    assert data[0]['name'] == course[rate_index].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'test'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    data = response.json()
    assert len(data) == 3
    assert data['name'] == 'test'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)
    rate_index = 0
    url = reverse('courses-detail', kwargs={"pk": course[rate_index].id})
    response = client.patch(url, {"name": "test"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data['name'] == 'test'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    assert Course.objects.count() == 1
    rate_index = 0
    url = reverse('courses-detail', kwargs={"pk": course[rate_index].id})
    response = client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.parametrize(['number_students', 'expected_status'],
                         ((15, True),
                          (21, False),
                          (17, True),
                          (20, True),
                          (30, False),))
@pytest.mark.django_db
def test_validation_maximum_students_course(settings, number_students,
                                            expected_status,
                                            django_assert_max_num_queries):
    course = Course.objects.create(name='course_test')
    limiter = settings.MAX_STUDENTS_PER_COURSE * 2
    try:
        with django_assert_max_num_queries(limiter) as captured:
            for i in range(number_students):
                course.students.create(name=f'student test №{i}')
        examination = len(captured.captured_queries) == number_students * 2
    except:
        examination = not expected_status
    assert examination
