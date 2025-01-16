import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.domain import Delivery as DeliveryDomain
from src.domain.atendimento import DeliveryDomainCreate
from src.models import Angel, Client, Delivery, Polo
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

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Delivery | None:
        pass

    def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Delivery]:
        if order_by_param not in self.available_order_by_dict.keys():
            raise ValueError(f"order_by_param must be one of {list(self.available_order_by_dict.keys())}")


        query = (
            select(Delivery)
            .join(Client, Delivery.cliente_id == Client.id)
            .join(Angel, Delivery.angel_id == Angel.id)
            .join(Polo, Delivery.polo_id == Polo.id)
            .order_by(self.available_order_by_dict[order_by_param])
            .filter(Delivery.deleted_at.is_(None))
        )
        paginated_query = db.paginate(
            query, page=page, per_page=per_page, error_out=False
        )

        return paginated_query.items  # type: ignore

    def create(self, data: DeliveryDomainCreate) -> Delivery:
        entity = Delivery(
            cliente_id=data.cliente_id,
            angel_id=data.id_angel,
            polo_id=data.id_polo,
            data_limite=data.data_limite,
            data_de_atendimento=data.data_de_atendimento,
        )

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

    def create_many(self, data: list[DeliveryDomain]) -> list[Delivery]:
        entities = [
            Delivery(
                cliente_id=item.cliente_id,
                angel_id=item.id_angel,
                polo_id=item.id_polo,
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

    def update(self, data: DeliveryDomain) -> Delivery | None:
        pass

    def delete(self, id: int) -> bool:
        raise NotImplementedError

    def get_by_attribute(self, attribute):
        raise NotImplementedError
