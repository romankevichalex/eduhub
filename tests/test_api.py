import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

suffix = uuid.uuid4().hex[:6]

# ───────────────────────────── AUTH ─────────────────────────────

def test_register_admin():
    response = client.post("/api/v1/auth/register", json={
        "email": f"admin_{suffix}@test.com",
        "first_name": "Admin",
        "last_name": "Test",
        "middle_name": "Middle",
        "password": "admin123",
        "role": "admin"
    })
    assert response.status_code == 200

def test_register_teacher():
    response = client.post("/api/v1/auth/register", json={
        "email": f"teacher_{suffix}@test.com",
        "first_name": "Teacher",
        "last_name": "Test",
        "middle_name": "Middle",
        "password": "teacher123",
        "role": "teacher"
    })
    assert response.status_code == 200

def test_register_student():
    response = client.post("/api/v1/auth/register", json={
        "email": f"student_{suffix}@test.com",
        "first_name": "Student",
        "last_name": "Test",
        "middle_name": "Middle",
        "password": "student123",
        "role": "student"
    })
    assert response.status_code == 200

def test_login_admin():
    response = client.post("/api/v1/auth/login", json={
        "email": f"admin_{suffix}@test.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/api/v1/auth/login", json={
        "email": "admin_test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_me():
    token = client.post("/api/v1/auth/login", json={
        "email": f"admin_{suffix}@test.com",
        "password": "admin123"
    }).json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={
        "authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == f"admin_{suffix}@test.com"

# ───────────────────────────── SUBJECTS ─────────────────────────────

@pytest.fixture
def admin_token():
    return client.post("/api/v1/auth/login", json={
        "email": f"admin_{suffix}@test.com",
        "password": "admin123"
    }).json()["access_token"]

@pytest.fixture
def teacher_token():
    return client.post("/api/v1/auth/login", json={
        "email": f"teacher_{suffix}@test.com",
        "password": "teacher123"
    }).json()["access_token"]

@pytest.fixture
def student_token():
    return client.post("/api/v1/auth/login", json={
        "email": f"student_{suffix}@test.com",
        "password": "student123"
    }).json()["access_token"]

@pytest.fixture
def subject_id(admin_token):
    response = client.post("/api/v1/subjects/", json={
        "name": "Тестовый предмет",
        "code": f"TEST-{uuid.uuid4().hex[:6]}",
        "description": "Описание"
    }, headers={"authorization": f"Bearer {admin_token}"})
    return response.json()["id"]

def test_create_subject(admin_token):
    response = client.post("/api/v1/subjects/", json={
        "name": "Математика",
        "code": f"MATH-{uuid.uuid4().hex[:6]}",
        "description": "Высшая математика"
    }, headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_create_subject_not_admin(student_token):
    response = client.post("/api/v1/subjects/", json={
        "name": "Математика",
        "code": "MATH998",
        "description": "Высшая математика"
    }, headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 403

def test_get_subjects():
    response = client.get("/api/v1/subjects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_subject_by_id(subject_id):
    response = client.get(f"/api/v1/subjects/{subject_id}")
    assert response.status_code == 200
    assert response.json()["id"] == subject_id

def test_update_subject(admin_token, subject_id):
    response = client.patch(f"/api/v1/subjects/{subject_id}", json={
        "name": "Обновлённый предмет"
    }, headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Обновлённый предмет"

def test_delete_subject(admin_token, subject_id):
    response = client.delete(f"/api/v1/subjects/{subject_id}",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204

# ───────────────────────────── ENROLLMENTS ─────────────────────────────

@pytest.fixture
def enrollment_id(student_token, subject_id):
    response = client.post("/api/v1/enrollments/", json={
        "subject_id": subject_id
    }, headers={"authorization": f"Bearer {student_token}"})
    return response.json()["id"]

def test_enroll_student(student_token, subject_id):
    response = client.post("/api/v1/enrollments/", json={
        "subject_id": subject_id
    }, headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    assert response.json()["subject_id"] == subject_id

def test_get_enrollments():
    response = client.get("/api/v1/enrollments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_enrollment(student_token, enrollment_id):
    response = client.delete(f"/api/v1/enrollments/{enrollment_id}",
        headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 204

# ───────────────────────────── POSTS ─────────────────────────────

@pytest.fixture
def post_id(teacher_token, subject_id):
    response = client.post(f"/api/v1/subjects/{subject_id}/posts", json={
        "content": "Тестовый пост"
    }, headers={"authorization": f"Bearer {teacher_token}"})
    return response.json()["id"]

def test_create_post(teacher_token, subject_id):
    response = client.post(f"/api/v1/subjects/{subject_id}/posts", json={
        "content": "Новый пост"
    }, headers={"authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "Новый пост"

def test_create_post_not_teacher(student_token, subject_id):
    response = client.post(f"/api/v1/subjects/{subject_id}/posts", json={
        "content": "Новый пост"
    }, headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 403

def test_get_posts(subject_id):
    response = client.get(f"/api/v1/subjects/{subject_id}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_comment(student_token, post_id):
    response = client.post(f"/api/v1/posts/{post_id}/comments", json={
        "content": "Тестовый комментарий"
    }, headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    assert response.json()["content"] == "Тестовый комментарий"

def test_get_comments(post_id):
    response = client.get(f"/api/v1/posts/{post_id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ───────────────────────────── CHAT ─────────────────────────────

def test_send_message(student_token, subject_id):
    response = client.post("/api/v1/chat/messages", json={
        "subject_id": subject_id,
        "message": "Привет, это тест"
    }, headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    assert response.json()["role"] == "assistant"

def test_get_chat_history(student_token, subject_id):
    response = client.get(f"/api/v1/chat/history?subject_id={subject_id}",
        headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    assert "messages" in response.json()

# ───────────────────────────── MATERIALS ─────────────────────────────

def test_create_material(teacher_token, subject_id):
    response = client.post("/api/v1/materials/", json={
        "subject_id": subject_id,
        "title": "Тестовый материал",
        "description": "Описание",
        "file_path": "/files/test.pdf",
        "file_type": "pdf"
    }, headers={"authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Тестовый материал"

def test_get_materials(subject_id):
    response = client.get(f"/api/v1/materials/?subject_id={subject_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_material(teacher_token, subject_id):
    material_id = client.post("/api/v1/materials/", json={
        "subject_id": subject_id,
        "title": "Для удаления",
        "description": "Описание",
        "file_path": "/files/delete.pdf",
        "file_type": "pdf"
    }, headers={"authorization": f"Bearer {teacher_token}"}).json()["id"]

    response = client.delete(f"/api/v1/materials/{material_id}",
        headers={"authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 204

# ───────────────────────────── ADMIN ─────────────────────────────

def test_admin_get_users(admin_token):
    response = client.get("/api/v1/admin/users",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_users_not_admin(student_token):
    response = client.get("/api/v1/admin/users",
        headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 403

def test_admin_verify_user(admin_token):
    register_response = client.post("/api/v1/auth/register", json={
        "email": f"verify_{uuid.uuid4().hex[:6]}@test.com",
        "first_name": "Verify",
        "last_name": "Test",
        "middle_name": "Middle",
        "password": "verify123",
        "role": "student"
    })
    student_id = register_response.json()["id"]
    response = client.patch(f"/api/v1/admin/users/{student_id}/verify",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["is_verified"] == True

def test_admin_get_subjects(admin_token):
    response = client.get("/api/v1/admin/subjects",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ───────────────────────────── ADMIN DELETE USER ─────────────────────────────

def test_admin_delete_user(admin_token):
    student_id = client.post("/api/v1/auth/register", json={
        "email": f"delete_{uuid.uuid4().hex[:6]}@test.com",
        "first_name": "Delete",
        "last_name": "Test",
        "middle_name": "Middle",
        "password": "delete123",
        "role": "student"
    }).json()["id"]

    response = client.delete(f"/api/v1/admin/users/{student_id}",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204

def test_admin_delete_user_not_found(admin_token):
    response = client.delete("/api/v1/admin/users/99999",
        headers={"authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404

def test_admin_delete_user_not_admin(student_token):
    response = client.delete("/api/v1/admin/users/1",
        headers={"authorization": f"Bearer {student_token}"})
    assert response.status_code == 403

# ───────────────────────────── MATERIALS GET BY ID ─────────────────────────────

def test_get_material_by_id(teacher_token, subject_id):
    material_id = client.post("/api/v1/materials/", json={
        "subject_id": subject_id,
        "title": "Тест материал",
        "description": "Описание",
        "file_path": "/files/test.pdf",
        "file_type": "pdf"
    }, headers={"authorization": f"Bearer {teacher_token}"}).json()["id"]

    response = client.get(f"/api/v1/materials/{material_id}")
    assert response.status_code == 200
    assert response.json()["id"] == material_id

def test_get_material_by_id_not_found():
    response = client.get("/api/v1/materials/99999")
    assert response.status_code == 404