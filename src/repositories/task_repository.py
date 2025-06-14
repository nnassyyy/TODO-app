import threading
from typing import Dict, List, Optional, Set
from src.domain.task import Task
from .base_repository import BaseRepository


class InMemoryTaskRepository(BaseRepository):
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._lock = threading.Lock()
        self._counter = 1

    def create(self, task: Task) -> Task:
        with self._lock:
            task.id = self._counter
            self._tasks[self._counter] = task
            self._counter += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task_id: int, task: Task) -> Optional[Task]:
        with self._lock:
            if task_id not in self._tasks:
                return None
            self._tasks[task_id] = task
            return task

    def delete(self, task_id: int) -> bool:
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def filter_tasks(
            self,
            tags: Optional[Set[str]] = None,
            completed: Optional[bool] = None,
            project_id: Optional[int] = None
    ) -> List[Task]:
        result = []
        for task in self._tasks.values():
            if completed is not None and task.is_completed != completed:
                continue
            if project_id is not None and task.project_id != project_id:
                continue
            if tags and not (tags & task.tags):  # Исправлено: используем пересечение множеств
                continue
            result.append(task)
        return result