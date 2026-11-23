import allure
import pytest

from src.api_client import ApiClient

BASE = "http://194.87.126.16"


@pytest.fixture(scope="module")
def client():
    return ApiClient(BASE)


@pytest.fixture
def student_id(client):
    # создаём студента перед тестом, удаляем после
    data = {
        "name": "Auto Student",
        "email": "auto.test@example.com",
        "phone_no": "+79990001122",
        "gender": "male",
        "status": 1,
    }
    r = client.create_student(data)
    assert r.status_code == 200
    sid = r.json()["student"]["id"]
    yield sid
    client.delete_student(sid)


@allure.epic("Students API")
@allure.feature("Students CRUD")
class TestStudents:

    @allure.title("get students list")
    def test_get_list(self, client):
        with allure.step("GET /student"):
            r = client.get_students()
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == 1
        assert isinstance(body.get("students"), list)
        assert len(body["students"]) > 0

    @allure.title("get student by id")
    def test_get_by_id(self, client, student_id):
        with allure.step(f"GET /student/{student_id}"):
            r = client.get_student(student_id)
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == 1
        assert body["student"]["id"] == student_id

    @allure.title("create student")
    def test_create(self, client):
        data = {
            "name": "New Student",
            "email": "new.student@example.com",
            "phone_no": "+79990001133",
            "gender": "female",
            "status": 1,
        }
        with allure.step("POST /student"):
            r = client.create_student(data)
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == 1
        s = body["student"]
        assert s["name"] == data["name"]
        assert s["id"] is not None
        # cleanup
        client.delete_student(s["id"])

    @allure.title("update student")
    def test_update(self, client, student_id):
        data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "phone_no": "+79990001122",
            "gender": "female",
            "status": 0,
        }
        with allure.step(f"PUT /student/{student_id}"):
            r = client.update_student(student_id, data)
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == 1, f"update failed: {body}"

    @allure.title("delete student")
    def test_delete(self, client, student_id):
        with allure.step(f"DELETE /student/{student_id}"):
            r = client.delete_student(student_id)
        assert r.status_code == 200
        with allure.step(f"GET /student/{student_id} after delete"):
            r = client.get_student(student_id)
        body = r.json()
        assert body.get("status") == 0, f"still exists: {body}"
