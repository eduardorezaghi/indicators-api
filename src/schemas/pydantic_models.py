from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class BaseModelSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None


class AtendimentoSchema(BaseModelSchema):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )

    id_cliente: int
    angel: Annotated[str, StringConstraints(max_length=255)]
    polo: Annotated[str, StringConstraints(max_length=255)]
    data_limite: datetime
    data_de_atendimento: datetime
