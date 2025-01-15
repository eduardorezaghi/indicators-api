import csv
from io import StringIO
from typing import Any

from flask import Blueprint, jsonify, request

from src.domain import Atendimento as AtendimentoDT

bp = Blueprint("atendimento", __name__)
# atendimento_service = AtendimentoService()

atendimentos: list[AtendimentoDT] = []


@bp.route("/import_csv", methods=["POST"])
async def import_csv() -> Any:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".csv"):
        decoded_stream = StringIO(file.stream.read().decode("UTF-8"))
        csv_input = csv.DictReader(decoded_stream, delimiter="\t")

        atendimentos.clear()
        for row in csv_input:
            obj = AtendimentoDT.from_dict(row)
            # atendimento = Atendimento(
            #     id=obj.id_atendimento,
            #     id_cliente=obj.id_cliente,
            #     angel=obj.angel,
            #     polo=obj.polo,
            #     data_limite=obj.data_limite,
            #     data_de_atendimento=obj.data_de_atendimento,
            # )
            atendimentos.append(obj)

        # await atendimento_service.create(atendimentos)
        return jsonify(
            {
                "message": "CSV file imported successfully",
                "data": [atendimento.__dict__ for atendimento in atendimentos],
            }
        ), 200

    return jsonify({"error": "Invalid file format"}), 400
