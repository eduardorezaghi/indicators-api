from typing import List

import werkzeug.exceptions

from src.database import default_db as db
from src.domain import Angel as AngelDomain
from src.domain import Client as ClientDomain
from src.domain import Delivery as DeliveryDomain
from src.domain import DeliveryDomainCreate, DeliveryDomainUpdate
from src.domain import Polo as PoloDomain
from src.models import Delivery
from src.repositories import (
    AngelRepository,
    ClientRepository,
    DeliveryRepository,
    PoloRepository,
)


class DeliveryService:
    # constructor injection for the repository (dependency injection)
    def __init__(
        self, repository: DeliveryRepository = DeliveryRepository(session=db.session)
    ):
        self.repository = repository

    def get_by_id(self, id: int) -> Delivery | None:
        return self.repository.get_by_id(id)

    def get_all(self, page: int, per_page: int, order_by_param: str) -> List[Delivery]:
        try:
            return self.repository.get_paginated(page, per_page, order_by_param)
        except ValueError as e:
            raise werkzeug.exceptions.BadRequest(
                description=f"Error getting the atendimentos: {str(e)}",
            )

    def create(self, atendimento: DeliveryDomain) -> Delivery:
        angel_repository = AngelRepository()
        polo_repository = PoloRepository()
        client_repository = ClientRepository()

        # check if the related entities exists.
        angel = angel_repository.get_by_name(atendimento.angel)
        polo = polo_repository.get_by_attribute(atendimento.polo)
        client = client_repository.get_by_id(atendimento.cliente_id)

        # if any of the related entities doesn't exist, create them.
        if angel is None:
            angel = angel_repository.create(AngelDomain(name=atendimento.angel))
        if polo is None:
            polo = polo_repository.create(PoloDomain(name=atendimento.polo))
        if client is None:
            client = client_repository.create(ClientDomain(id=atendimento.cliente_id))

        try:
            # Create the atendimento
            atendimento_create = DeliveryDomainCreate(
                cliente_id=client.id,  # type: ignore
                id_angel=angel.id,  # type: ignore
                id_polo=polo.id,  # type: ignore
                data_limite=atendimento.data_limite,
                data_de_atendimento=atendimento.data_de_atendimento,
            )
        except Exception as e:
            raise werkzeug.exceptions.BadRequest(
                description=f"Error creating the atendimento: {str(e)}",
            )

        return self.repository.create(atendimento_create)

    def create_many(self, atendimentos: List[DeliveryDomain]) -> List[Delivery]:
        return self.repository.create_many(atendimentos)

    def update(
        self, atendimento: DeliveryDomainUpdate, id: int = None
    ) -> Delivery | None:
        return self.repository.update(atendimento, id)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def get_angel_productivity(self, at_most: int) -> List[dict]:
        try:
            sequence = self.repository.get_angel_productivity_view(at_most)
        except Exception as e:
            raise werkzeug.exceptions.InternalServerError(
                description=f"Error getting the angel productivity: {str(e)}",
                original_exception=e,
            )

        serialized_items = []
        for row in sequence:
            item = {
                "angel": row[0],
                "total_deliveries": row[1],
                "on_time_deliveries": row[2],
                "on_time_percentage": row[3],
            }
            serialized_items.append(item)

        return serialized_items

    def get_polo_productivity(self, at_most: int) -> List[dict]:
        try:
            sequence = self.repository.get_polo_productivity_view(at_most)
        except Exception as e:
            raise werkzeug.exceptions.InternalServerError(
                description=f"Error getting the polo productivity: {str(e)}",
                original_exception=e,
            )

        serialized_items = []
        for row in sequence:
            item = {
                "polo": row[0],
                "weekday": row[1],
                "total_deliveries": row[2],
            }
            serialized_items.append(item)

        return serialized_items
