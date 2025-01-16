# mypy: ignore-errors

import http
import io
from datetime import datetime

import pytest

from src.api.atendimento_routes import atendimentos
from src.models import Delivery


class TestDeliveryRoutes:
    def test_query_all_atendimentos(self, client, atendimentos_fixture: list[Delivery]):
        response = client.get("/api/v1/atendimento")
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert len(json_response.get("data")) == 2

    def test_query_all_atendimentos_with_pagination(
        self, client, atendimentos_fixture: list[Delivery]
    ):
        response = client.get("/api/v1/atendimento?page=1&per_page=1")
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert len(json_response.get("data")) == 1

    def test_query_all_atendimentos_with_invalid_order_by(
        self, client, atendimentos_fixture: list[Delivery]
    ):
        response = client.get("/api/v1/atendimento?order_by=invalid")
        json_response = response.json

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert (
            json_response.get("error")
            == "order_by_param must be one of ['id', 'created_at', 'updated_at', 'id_cliente', 'angel', 'polo', 'data_limite', 'data_de_atendimento']"
        )

    def test_query_all_atendimentos_shouldnt_return_deleted_at_items(
        self, client, atendimentos_fixture: list[Delivery]
    ):
        atendimentos_fixture[0].deleted_at = datetime(2021, 6, 29, 0, 0, 0)
        atendimentos_fixture[1].deleted_at = datetime(2021, 6, 29, 0, 0, 0)

        response = client.get("/api/v1/atendimento")
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert len(json_response.get("data")) == 0

    def test_create_atendimento(self, client):
        data = {
            "cliente_id": 123456,
            "angel": "John Doe",
            "polo": "SP - SÃO PAULO",
            "data_limite": "2021-06-30",
            "data_de_atendimento": "2021-06-29",
        }

        response = client.post("/api/v1/atendimento", json=data)
        json_response = response.json

        assert response.status_code == http.HTTPStatus.CREATED
        assert json_response["cliente_id"] == data["cliente_id"]
        assert json_response["angel"] == data["angel"]
        assert json_response["polo"] == data["polo"]
        assert json_response["data_limite"] is not None
        assert json_response["data_de_atendimento"] is not None

    def test_create_atendimento_missing_data(self, client):
        data = {
            "cliente_id": 123456,
            "angel": "John Doe",
        }

        response = client.post("/api/v1/atendimento", json=data)
        json_response = response.json

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert "error" in json_response

    def test_import_csv_no_file(self, client):
        response = client.post("/api/v1/atendimento/import_csv")
        assert response.status_code == 400
        assert response.json == {"error": "No file part"}

    def test_import_csv_successfully_processed_csv(self, client):
        csv_content = """id_atendimento\tid_cliente\tangel\tpolo\tdata_limite\tdata_de_atendimento
715\t77226365\tSergio Wanderley Ferreira\tCE - JUAZEIRO DO NORTE\t30/06/2021\t2021-06-29 09:09:30
667\t968422633\tJônatas Neves Bandoli\tPR - CURITIBA\t30/06/2021\t2021-06-28 09:01:19
"""
        data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}

        response = client.post(
            "/api/v1/atendimento/import_csv",
            data=data,
            content_type="multipart/form-data",
        )
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert json_response.get("message") == "CSV file imported successfully"
        assert len(atendimentos) == 2
        assert atendimentos[0].id == 715
        assert atendimentos[1].id == 667

    @pytest.mark.parametrize("delimiter", [",", ";", "\t"])
    def test_import_csv_with_various_delimiters(self, client, delimiter):
        csv_content = f"""id_atendimento{delimiter}id_cliente{delimiter}angel{delimiter}polo{delimiter}data_limite{delimiter}data_de_atendimento
715{delimiter}77226365{delimiter}Sergio Wanderley Ferreira{delimiter}CE - JUAZEIRO DO NORTE{delimiter}30/06/2021{delimiter}2021-06-29 09:09:30
667{delimiter}968422633{delimiter}Jônatas Neves Bandoli{delimiter}PR - CURITIBA{delimiter}30/06/2021{delimiter}2021-06-28 09:01:19
"""
        data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}

        response = client.post(
            "/api/v1/atendimento/import_csv",
            data=data,
            content_type="multipart/form-data",
        )
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert json_response.get("message") == "CSV file imported successfully"
        assert len(atendimentos) == 2
        assert atendimentos[0].id == 715
        assert atendimentos[1].id == 667

    @pytest.mark.parametrize("date_format", [
        "2021/06/29 09:09:30", 
        "2021-06-29 09:09:30", 
        "29/06/2021 09:09:30", 
        "29-06-2021 09:09:30"
    ])
    def test_import_csv_with_other_date_format(self, client, date_format):
        csv_content = f"""id_atendimento,id_cliente,angel,polo,data_limite,data_de_atendimento
715,77226365,Sergio Wanderley Ferreira,CE - JUAZEIRO DO NORTE,30/06/2021,{date_format}
667,968422633,Jônatas Neves Bandoli,PR - CURITIBA,30/06/2021,{date_format}
"""
        data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}

        response = client.post(
            "/api/v1/atendimento/import_csv",
            data=data,
            content_type="multipart/form-data",
        )
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert json_response.get("message") == "CSV file imported successfully"
        assert len(atendimentos) == 2
        assert atendimentos[0].id == 715
        assert atendimentos[1].id == 667

    def test_import_csv_invalid_data_de_atendimento_date(self, client):
        csv_content = """id_atendimento,id_cliente,angel,polo,data_limite,data_de_atendimento
715,77226365,Sergio Wanderley Ferreira,CE - JUAZEIRO DO NORTE,30/06/2021,29/062021 09:09:30
"""
        data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}

        response = client.post(
            "/api/v1/atendimento/import_csv",
            data=data,
            content_type="multipart/form-data",
        )
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert any("Invalid CSV file at line 2" in error for error in json_response.get("errors"))

    def test_import_csv_invalid_data_de_atendimento_third_row(self, client):
        csv_content = """id_atendimento,id_cliente,angel,polo,data_limite,data_de_atendimento
715,77226365,Sergio Wanderley Ferreira,CE - JUAZEIRO DO NORTE,30/06/2021,2021-06-29 09:09:30
668,968422633,Jônatas Neves Bandoli,PR - CURITIBA,30/06/2021,28/062021 09:01:19
"""
        data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}

        response = client.post(
            "/api/v1/atendimento/import_csv",
            data=data,
            content_type="multipart/form-data",
        )
        json_response = response.json

        assert response.status_code == http.HTTPStatus.OK
        assert any("Invalid CSV file at line 3" in error for error in json_response.get("errors"))
        assert len(atendimentos) == 1
        assert atendimentos[0].id == 715