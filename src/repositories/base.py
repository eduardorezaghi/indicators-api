from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_by_attribute(self, attribute: Any) -> T | None:
        pass

    @abstractmethod
    async def get_by_attribute_async(self, attribute: Any) -> T | None:
        pass

    @abstractmethod
    async def get_by_id_async(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T | None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
