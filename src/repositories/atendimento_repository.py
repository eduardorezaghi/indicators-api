import datetime
from typing import Sequence

import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.domain import Delivery as DeliveryDomain
from src.domain.atendimento import DeliveryDomainCreate, DeliveryDomainUpdate
from src.models import (
    Angel,
    Client,
    Delivery,
    Polo,
    angel_productivity_view,
    polo_productivity_view,
)
from src.repositories.base import BaseRepository


class DeliveryRepository(BaseRepository[Delivery]):
    available_order_by_dict = {
        "id": Delivery.id,
        "-id": Delivery.id.desc(),
        "created_at": Delivery.created_at,
        "-created_at": Delivery.created_at.desc(),
        "updated_at": Delivery.updated_at,
        "-updated_at": Delivery.updated_at.desc(),
        "cliente_id": Delivery.cliente_id,
        "-cliente_id": Delivery.cliente_id.desc(),
        "angel": Angel.name,
        "-angel": Angel.name.desc(),
        "polo": Polo.name,
        "-polo": Polo.name.desc(),
        "data_limite": Delivery.data_limite,
        "-data_limite": Delivery.data_limite.desc(),
        "data_de_atendimento": Delivery.data_de_atendimento,
        "-data_de_atendimento": Delivery.data_de_atendimento.desc(),
    }

    # constructor injection for the session (dependency injection)
    def __init__(
        self, session: Session = db.session, async_session: AsyncSession = None
    ):
        self.session = session
        self.async_session = async_session

    def get_by_id(self, id: int) -> Delivery | None:
        entity = (
            self.session.query(Delivery)
            .filter(Delivery.id == id, Delivery.deleted_at.is_(None))
            .first()
        )

        return entity

    def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Delivery]:
        if order_by_param not in self.available_order_by_dict.keys():
            raise ValueError(
                f"order_by_param must be one of {list(self.available_order_by_dict.keys())}"
            )

        query = (
            select(Delivery)
            .join(Client, Delivery.cliente_id == Client.id)
            .join(Angel, Delivery.id_angel == Angel.id)
            .join(Polo, Delivery.id_polo == Polo.id)
            .order_by(self.available_order_by_dict[order_by_param])
            .filter(Delivery.deleted_at.is_(None))
        )
        paginated_query = db.paginate(
            query, page=page, per_page=per_page, error_out=False
        )

        return paginated_query.items  # type: ignore

    def create(self, data: DeliveryDomainCreate) -> Delivery:
        entity = Delivery(**data.to_dict())

        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def create_async(self, data: DeliveryDomainCreate) -> Delivery:
        entity = Delivery(
            id=data.id,
            cliente_id=data.cliente_id,
            id_angel=data.id_angel,
            id_polo=data.id_polo,
            data_limite=data.data_limite,
            data_de_atendimento=data.data_de_atendimento,
        )

        try:
            self.async_session.add(entity)
            await self.async_session.commit()
            await self.async_session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def bulk_create_async(
        self, data: list[DeliveryDomainCreate]
    ) -> list[Delivery]:
        entities = [
            Delivery(
                cliente_id=item.cliente_id,
                id_angel=item.id_angel,
                id_polo=item.id_polo,
                data_limite=item.data_limite,
                data_de_atendimento=item.data_de_atendimento,
            )
            for item in data
        ]

        try:
            self.async_session.add_all(entities)
            await self.async_session.commit()
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entities.",
                original_exception=e,
            )

        return entities

    def create_many(self, data: list[DeliveryDomain]) -> list[Delivery]:
        entities = [
            Delivery(
                cliente_id=item.cliente_id,
                id_angel=item.id_angel,
                id_polo=item.id_polo,
                data_limite=item.data_limite,
                data_de_atendimento=item.data_de_atendimento,
            )
            for item in data
        ]

        try:
            self.session.bulk_save_objects(entities)
            self.session.commit()
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise Exception(
                "An error occurred while trying to create the entities.",
                e,
            )

        return entities

    def update(self, data: DeliveryDomainUpdate, id: int = None) -> Delivery | None:
        entity = self.get_by_id(data.id if id is None else id)
        if entity is None:
            return None

        entity.updated_at = datetime.datetime.now(datetime.UTC)
        entity.data_limite = data.data_limite
        entity.data_de_atendimento = data.data_de_atendimento

        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to update the entity.",
                original_exception=e,
            )

        return entity

    def get_angel_productivity_view(self, at_most: int) -> Sequence[Row]:
        stmt = select(angel_productivity_view).limit(at_most)
        items = self.session.execute(stmt).fetchall()

        return items

    def get_polo_productivity_view(self, at_most: int) -> Sequence[Row]:
        stmt = select(polo_productivity_view).limit(at_most)
        items = self.session.execute(stmt).fetchall()

        return items

    def delete(self, id: int) -> bool:
        raise NotImplementedError

    def get_by_attribute(self, attribute):
        raise NotImplementedError

    async def get_by_attribute_async(self, attribute):
        raise NotImplementedError

    async def get_by_id_async(self, id):
        raise NotImplementedError
