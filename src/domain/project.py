from .entities import BaseEntity


class Project(BaseEntity):
    def __init__(self, title: str, description: str = ""):
        super().__init__(title)
        self.description = description
        self.is_active = True

    def archive(self) -> None:
        if self.is_active:
            self.is_active = False
            self._add_history("Project archived")

    def activate(self) -> None:
        if not self.is_active:
            self.is_active = True
            self._add_history("Project activated")