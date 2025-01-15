# mypy: ignore-errors

import http
import io

import pytest

from src.api.atendimento_routes import atendimentos


class TestAtendimentoRoutes:
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
        assert atendimentos[0].id_atendimento == 715
        assert atendimentos[1].id_atendimento == 667
