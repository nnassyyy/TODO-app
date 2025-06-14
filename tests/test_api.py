import pytest
from fastapi.testclient import TestClient
from src.api.server import app
from src.api.dependencies import get_task_repository, get_project_repository
from src.repositories.task_repository import InMemoryTaskRepository
from src.repositories.project_repository import InMemoryProjectRepository

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repositories():
    task_repo = get_task_repository()
    project_repo = get_project_repository()

    task_repo._tasks = {}
    task_repo._counter = 1

    project_repo._projects = {}
    project_repo._counter = 1

def test_create_task():
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "tags": ["test"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert "test" in data["tags"]
    assert data["id"] == 1

def test_get_task():
    client.post("/api/v1/tasks", json={"title": "Get test"})
    response = client.get("/api/v1/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get test"
    assert data["id"] == 1

def test_task_history():
    client.post("/api/v1/tasks", json={"title": "History test"})
    client.patch("/api/v1/tasks/1", json={"title": "Updated title"})
    response = client.get("/api/v1/tasks/1/history")
    assert response.status_code == 200
    history = response.json()
    assert len(history) >= 2
    assert "created" in history[0].lower()
    assert "title changed" in history[1].lower()

def test_filter_tasks_by_tags():
    client.post("/api/v1/tasks", json={"title": "Task 1", "tags": ["urgent", "important"]})
    client.post("/api/v1/tasks", json={"title": "Task 2", "tags": ["important"]})
    response = client.get("/api/v1/tasks?tags=urgent")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"

def test_create_project():
    response = client.post(
        "/api/v1/projects",
        json={"title": "Test project", "description": "Test description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test project"
    assert data["description"] == "Test description"
    assert data["is_active"] is True

def test_get_project_tasks():
    project_response = client.post(
        "/api/v1/projects",
        json={"title": "Project with tasks"}
    )
    project_id = project_response.json()["id"]

    client.post(
        "/api/v1/tasks",
        json={"title": "Project task 1", "project_id": project_id}
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Project task 2", "project_id": project_id}
    )

    response = client.get(f"/api/v1/projects/{project_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Project task 1"
    assert tasks[1]["title"] == "Project task 2"