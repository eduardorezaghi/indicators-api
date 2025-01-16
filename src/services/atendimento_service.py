from typing import List

from src.domain import Delivery as DeliveryDomain
from src.models import Delivery
from src.repositories.atendimento_repository import DeliveryRepository


class DeliveryService:
    def __init__(self, repository: DeliveryRepository = DeliveryRepository()):
        self.repository = repository

    async def get_by_id(self, id: int) -> Delivery | None:
        return await self.repository.get_by_id(id)

    async def get_all(
        self, page: int, per_page: int, order_by_param: str
    ) -> List[Delivery]:
        try:
            return await self.repository.get_paginated(page, per_page, order_by_param)
        except ValueError as e:
            raise ValueError(e)

    async def create(self, atendimento: DeliveryDomain) -> Delivery:
        return await self.repository.create(atendimento)

    async def create_many(self, atendimentos: List[DeliveryDomain]) -> List[Delivery]:
        return await self.repository.create_many(atendimentos)

    async def update(self, atendimento: DeliveryDomain) -> Delivery | None:
        return await self.repository.update(atendimento)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
