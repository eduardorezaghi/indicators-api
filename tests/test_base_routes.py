# mypy: ignore-errors

import http
import json


class TestBase:
    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == http.HTTPStatus.OK
        assert response.data == b"Hello, World!"

    def test_echo_with_json(self, client):
        test_data = {"message": "test"}
        response = client.get("/echo", data=json.dumps(test_data))
        assert response.status_code == http.HTTPStatus.OK
        assert response.json == test_data

    def test_echo_without_data(self, client):
        response = client.get("/echo")

        print(response.data)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST
