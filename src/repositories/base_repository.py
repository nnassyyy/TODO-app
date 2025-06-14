from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class BaseRepository(ABC):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass