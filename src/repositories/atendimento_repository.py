import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select

from src.database import default_db as db
from src.domain import Delivery as DeliveryDomain
from src.domain.atendimento import DeliveryDomainCreate
from src.models import Angel, Client, Delivery, Polo
from src.repositories.base import BaseRepository


class DeliveryRepository(BaseRepository[Delivery]):
    available_order_by = [
        "id",
        "created_at",
        "updated_at",
        "id_cliente",
        "angel",
        "polo",
        "data_limite",
        "data_de_atendimento",
    ]

    async def get_by_id(self, id: int) -> Delivery | None:
        pass

    async def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Delivery]:
        if order_by_param not in self.available_order_by:
            raise ValueError(f"order_by_param must be one of {self.available_order_by}")

        query = (
            select(Delivery)
            .join(Client, Delivery.cliente_id == Client.id)
            .join(Angel, Delivery.angel_id == Angel.id)
            .join(Polo, Delivery.polo_id == Polo.id)
            .order_by(order_by_param)
            .filter(Delivery.deleted_at.is_(None))
        )
        paginated_query = db.paginate(
            query, page=page, per_page=per_page, error_out=False
        )

        return paginated_query.items

    async def create(self, data: DeliveryDomainCreate) -> Delivery:
        entity = Delivery(
            cliente_id=data.cliente_id,
            angel_id=data.id_angel,
            polo_id=data.id_polo,
            data_limite=data.data_limite,
            data_de_atendimento=data.data_de_atendimento,
        )

        try:
            with db.session() as session:
                session.add(entity)
                session.commit()
                session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def create_many(self, data: list[DeliveryDomain]) -> list[Delivery]:
        entities = []
        with db.session() as session:
            for item in data:
                entity = Delivery(**item.to_dict())
                entities.append(entity)

            session.add_all(entities)

        return entities

    async def update(self, data: DeliveryDomain) -> Delivery | None:
        pass

    async def delete(self, id: int) -> bool:
        raise NotImplementedError

    async def get_by_attribute(self, attribute):
        raise NotImplementedError
