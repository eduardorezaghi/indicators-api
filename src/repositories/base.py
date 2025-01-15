from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    async def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T | None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
