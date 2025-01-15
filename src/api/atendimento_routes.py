import csv
from io import StringIO
from typing import Any

from flask import Blueprint, jsonify, request, url_for

from src.domain import Atendimento as AtendimentoDT
from src.schemas import AtendimentoSchema
from src.services.atendimento_service import AtendimentoService

bp = Blueprint("atendimento", __name__)

atendimentos: list[AtendimentoDT] = []
errors: list[str] = []

@bp.route("", methods=["GET"])
async def get_all() -> Any:
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    order_by_param = request.args.get("order_by", default="id", type=str)

    atendimento_service = AtendimentoService()
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

    dump_items = [
        AtendimentoSchema.model_validate(atendimento) for atendimento in atendimentos
    ]
    serialized_items = [item.model_dump() for item in dump_items]

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
                obj = AtendimentoDT.from_dict(row)
            except Exception as e:
                errors.append(f"Invalid CSV file at line {line_number}: {e}")
                continue
            atendimentos.append(obj)

        # await atendimento_service.create(atendimentos)
        return jsonify(
            {
                "message": "CSV file imported successfully",
                "data": [atendimento.__dict__ for atendimento in atendimentos],
                "errors": errors,
            }
        ), 200
