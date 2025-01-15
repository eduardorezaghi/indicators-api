from io import StringIO
from typing import List

from sqlalchemy.orm.session import Session

from src.domain import Atendimento as AtendimentoDomain
from src.models import Atendimento
from src.repositories.atendimento_repository import AtendimentoRepository


class AtendimentoService:
    def __init__(self, repository: AtendimentoRepository = AtendimentoRepository()):
        self.repository = repository

    async def get_by_id(self, id: int) -> Atendimento | None:
        return await self.repository.get_by_id(id)

    async def get_all(
        self, page: int, per_page: int, order_by_param: str
    ) -> List[Atendimento]:
        try:
            return await self.repository.get_paginated(page, per_page, order_by_param)
        except ValueError as e:
            raise ValueError(e)

    async def create(self, atendimento: AtendimentoDomain) -> Atendimento:
        return await self.repository.create(atendimento)

    async def create_many(
        self, atendimentos: List[AtendimentoDomain]
    ) -> List[Atendimento]:
        return await self.repository.create_many(atendimentos)

    async def update(self, atendimento: AtendimentoDomain) -> Atendimento | None:
        return await self.repository.update(atendimento)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
