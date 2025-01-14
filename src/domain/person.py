from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    name: str
    birth_date: datetime
    email: str
    phone: str
    address: str
