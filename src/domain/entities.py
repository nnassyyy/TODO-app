from datetime import datetime
from typing import List, Optional


class BaseEntity:
    def __init__(self, title: str):
        self._validate_title(title)
        self.id: Optional[int] = None
        self.title = title
        self.created_at = datetime.now()
        self.history: List[str] = []
        self._add_history("Entity created")

    def _validate_title(self, title: str) -> None:
        if len(title) < 3:
            raise ValueError("Title must be at least 3 characters")

    def _add_history(self, event: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp}: {event}")

    def update_title(self, new_title: str) -> None:
        self._validate_title(new_title)
        self._add_history(f"Title changed: {self.title} → {new_title}")
        self.title = new_title