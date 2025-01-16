# mypy: ignore-errors

import http
import io
from datetime import datetime

import pytest

from src.api.atendimento_routes import atendimentos
from src.models import Delivery
from src.repositories import DeliveryRepository


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
            == f"order_by_param must be one of {list(DeliveryRepository.available_order_by_dict.keys())}"
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
