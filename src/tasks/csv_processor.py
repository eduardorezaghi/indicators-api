import csv
from io import StringIO

import asyncio
from celery import shared_task

from src.database import get_celery_session
from src.domain import Delivery as DeliveryDT
from src.domain import Angel as AngelDomain
from src.domain import Client as ClientDomain
from src.domain import Polo as PoloDomain
from src.repositories import DeliveryRepository, AngelRepository, PoloRepository, ClientRepository


@shared_task
def import_csv_task(file_content: str) -> dict:
    with get_celery_session() as session:
        with StringIO(file_content) as decoded_stream:
            sample = decoded_stream.read(1024)
            decoded_stream.seek(0)
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            decoded_stream.seek(0)

            csv_input = csv.DictReader(decoded_stream, delimiter=dialect.delimiter)
            atendimento_repository = DeliveryRepository(session)
            angel_repository = AngelRepository(session)
            polo_repository = PoloRepository(session)
            client_repository = ClientRepository(session)

            for _, row in enumerate(csv_input, start=2):
                obj = DeliveryDT.from_dict(row)

                # Check if related entities exist
                angel = angel_repository.get_by_name(obj.angel)
                polo = polo_repository.get_by_attribute(obj.polo)
                client = client_repository.get_by_id(obj.cliente_id)

                # If any of the related entities doesn't exist, create them
                if angel is None:
                    angel = angel_repository.create(AngelDomain(name=obj.angel))
                if polo is None:
                    polo = polo_repository.create(PoloDomain(name=obj.polo))
                if client is None:
                    client = client_repository.create(ClientDomain(id=obj.cliente_id))

                obj.id_angel = angel.id
                obj.id_polo = polo.id
                obj.cliente_id = client.id
                
                try:
                    atendimento_repository.create(obj)
                except Exception as e:
                    print(f"Error on line {row}: {e}")
                    continue


    return {
        "status": "success",
        "message": "CSV imported successfully.",
    }
