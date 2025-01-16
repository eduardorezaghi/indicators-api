import csv
from io import StringIO
from typing import Any

import werkzeug.exceptions
from flask import Blueprint, jsonify, request, url_for

from src.domain import Delivery as DeliveryDT
from src.services.atendimento_service import DeliveryService

bp = Blueprint("atendimento", __name__)

atendimentos: list[DeliveryDT] = []
errors: list[str] = []


@bp.route("", methods=["POST"])
async def create() -> Any:
    data = request.get_json()

    try:
        atendimento = DeliveryDT.from_dict(data)
    except Exception as e:
        raise werkzeug.exceptions.BadRequest(str(e))

    # check if any needed field is missing
    if not atendimento.cliente_id or not atendimento.angel or not atendimento.polo:
        raise werkzeug.exceptions.BadRequest("Missing required fields")


    delivery_service = DeliveryService()

    entity = await delivery_service.create(atendimento)
    item = atendimento.__dict__
    item["id"] = entity.id

    return jsonify(item), 201


@bp.route("", methods=["GET"])
async def get_all() -> Any:
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    order_by_param = request.args.get("order_by", default="id", type=str)

    atendimento_service = DeliveryService()
    try:
        atendimentos = await atendimento_service.get_all(page, per_page, order_by_param)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    next_page = (
        url_for(
            "atendimento.get_all",
            page=page + 1,
            per_page=per_page,
            order_by=order_by_param,
        )
        if len(atendimentos) == per_page
        else None
    )
    prev_page = (
        url_for(
            "atendimento.get_all",
            page=page - 1,
            per_page=per_page,
            order_by=order_by_param,
        )
        if page > 1
        else None
    )

    serialized_items = []
    for atendimento in atendimentos:
        item = DeliveryDT(
            id=atendimento.id,
            cliente_id=atendimento.cliente_id,
            angel=atendimento.angel.name,
            polo=atendimento.polo.name,
            data_limite=atendimento.data_limite,
            data_de_atendimento=atendimento.data_de_atendimento,
        )
        serialized_items.append(item.__dict__)

    return jsonify(
        {
            "data": serialized_items,
            "next": next_page,
            "prev": prev_page,
        }
    )


@bp.route("/import_csv", methods=["POST"])
async def import_csv() -> Any:
    if "file" not in request.files and not request.data:
        return jsonify({"error": "No file part"}), 400

    file = request.files.get("file")
    if file:
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        file_content = file.stream.read().decode("UTF-8")
    else:
        file_content = request.data.decode("UTF-8")

    if not file_content:
        return jsonify({"error": "Empty file"}), 400

    with StringIO(file_content) as decoded_stream:
        sample = decoded_stream.read(1024)
        decoded_stream.seek(0)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        decoded_stream.seek(0)

        csv_input = csv.DictReader(decoded_stream, delimiter=dialect.delimiter)

        atendimentos.clear()
        errors.clear()
        for line_number, row in enumerate(csv_input, start=2):
            try:
                obj = DeliveryDT.from_dict(row)
            except Exception as e:
                errors.append(f"Invalid CSV file at line {line_number}: {e}")
                continue
            atendimentos.append(obj)

        # atendimento_service = DeliveryService()
        # await atendimento_service.create_many(atendimentos)
        return jsonify(
            {
                "message": "CSV file imported successfully",
                "data": [atendimento.__dict__ for atendimento in atendimentos],
                "errors": errors,
            }
        ), 200
