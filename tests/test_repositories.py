from datetime import datetime
from typing import List, Set, Optional
from src.domain.entities import BaseEntity


class Task(BaseEntity):
    def __init__(self, title: str, project_id: Optional[int] = None):
        super().__init__(title)
        self.project_id = project_id
        self.tags: Set[str] = set()

    def add_tag(self, tag: str) -> None:
        if len(tag) < 2:
            raise ValueError("Tag must be at least 2 characters")
        if tag not in self.tags:
            self.tags.add(tag)
            self._add_history(f"Tag added: {tag}")

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
            self._add_history(f"Tag removed: {tag}")

    def get_history(self) -> List[str]:
        return self.history.copy()  # Защищаем от внешнего изменения