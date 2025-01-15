from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import default_db as db
from src.domain import Atendimento as AtendimentoDomain
from src.models.atendimento import Atendimento
from src.repositories.base import BaseRepository


class AtendimentoRepository(BaseRepository[Atendimento]):
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

    async def get_by_id(self, id: int) -> Atendimento | None:
        pass

    async def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Atendimento]:
        if order_by_param not in self.available_order_by:
            raise ValueError(f"order_by_param must be one of {self.available_order_by}")

        query = (
            select(Atendimento)
            .order_by(order_by_param)
            .filter(Atendimento.deleted_at.is_(None))
        )
        paginated_query = db.paginate(
            query, page=page, per_page=per_page, error_out=False
        )

        return paginated_query.items

    async def create(self, data: AtendimentoDomain) -> Atendimento:
        dict_data = data.to_dict()
        entity = Atendimento(**dict_data)

        with db.session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

        return entity

    async def create_many(self, data: list[AtendimentoDomain]) -> list[Atendimento]:
        entities = []
        with db.session() as session:
            for item in data:
                entity = Atendimento(**item.to_dict())
                entities.append(entity)

            session.add_all(entities)

        return entities

    async def update(self, data: AtendimentoDomain) -> Atendimento | None:
        pass

    async def delete(self, id: int) -> bool:
        pass
