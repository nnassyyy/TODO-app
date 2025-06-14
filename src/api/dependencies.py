from src.repositories.task_repository import InMemoryTaskRepository
from src.repositories.project_repository import InMemoryProjectRepository

# Создаем экземпляры репозиториев
task_repo = InMemoryTaskRepository()
project_repo = InMemoryProjectRepository()

def get_task_repository():
    return task_repo

def get_project_repository():
    return project_repo