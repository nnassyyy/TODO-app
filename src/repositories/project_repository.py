import threading
from typing import Dict, List, Optional
from src.domain.project import Project
from .base_repository import BaseRepository


class InMemoryProjectRepository(BaseRepository):
    def __init__(self):
        self._projects: Dict[int, Project] = {}
        self._lock = threading.Lock()
        self._counter = 1

    def create(self, project: Project) -> Project:
        with self._lock:
            project.id = self._counter
            self._projects[self._counter] = project
            self._counter += 1
        return project

    def get(self, project_id: int) -> Optional[Project]:
        return self._projects.get(project_id)

    def get_all(self) -> list[Project]:
        return list(self._projects.values())

    def update(self, project_id: int, project: Project) -> Optional[Project]:
        with self._lock:
            if project_id not in self._projects:
                return None
            self._projects[project_id] = project
            return project

    def delete(self, project_id: int) -> bool:
        with self._lock:
            if project_id in self._projects:
                del self._projects[project_id]
                return True
            return False

    def get_active(self) -> list[Project]:
        return [p for p in self._projects.values() if p.is_active]