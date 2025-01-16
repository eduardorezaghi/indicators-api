from typing import List

from src.domain import Angel as AngelDomain
from src.domain import Client as ClientDomain
from src.domain import Delivery as DeliveryDomain
from src.domain import DeliveryDomainCreate
from src.domain import Polo as PoloDomain
from src.models import Delivery
from src.repositories import (
    AngelRepository,
    ClientRepository,
    DeliveryRepository,
    PoloRepository,
)


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
        angel_repository = AngelRepository()
        polo_repository = PoloRepository()
        client_repository = ClientRepository()

        # check if the related entities exists.
        angel = await angel_repository.get_by_name(atendimento.angel)
        polo = await polo_repository.get_by_attribute(atendimento.polo)
        client = await client_repository.get_by_id(atendimento.cliente_id)

        # if any of the related entities doesn't exist, create them.
        if angel is None:
            angel = await angel_repository.create(AngelDomain(name=atendimento.angel))
        if polo is None:
            polo = await polo_repository.create(PoloDomain(name=atendimento.polo))
        if client is None:
            client = await client_repository.create(
                ClientDomain(id=atendimento.cliente_id)
            )

        # Create the atendimento
        atendimento_create = DeliveryDomainCreate(
            cliente_id=client.id,  # type: ignore
            id_angel=angel.id,  # type: ignore
            id_polo=polo.id,  # type: ignore
            data_limite=atendimento.data_limite,
            data_de_atendimento=atendimento.data_de_atendimento,
        )

        return await self.repository.create(atendimento_create)

    async def create_many(self, atendimentos: List[DeliveryDomain]) -> List[Delivery]:
        return await self.repository.create_many(atendimentos)

    async def update(self, atendimento: DeliveryDomain) -> Delivery | None:
        return await self.repository.update(atendimento)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
