
from src.database import default_db
from src.models.base_model import BaseModel


# mypy: ignore-errors
class Client(BaseModel, default_db.Model):
    __tablename__ = "cliente"
