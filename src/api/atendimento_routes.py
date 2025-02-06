from typing import Any

import werkzeug.exceptions
from celery.result import AsyncResult
from flask import Blueprint, jsonify, request, url_for

from src.domain import Delivery as DeliveryDT
from src.domain import DeliveryDomainUpdate
from src.services.atendimento_service import DeliveryService
from src.tasks import import_csv_task

bp = Blueprint("atendimento", __name__)

atendimentos: list[DeliveryDT] = []
errors: list[str] = []


@bp.route("", methods=["POST"])
def create() -> Any:
    data = request.get_json()

    try:
        atendimento = DeliveryDT.from_dict(data)
    except Exception as e:
        raise werkzeug.exceptions.BadRequest(str(e))

    # check if any needed field is missing
    if not atendimento.cliente_id or not atendimento.angel or not atendimento.polo:
        raise werkzeug.exceptions.BadRequest("Missing required fields")

    delivery_service = DeliveryService()

    entity = delivery_service.create(atendimento)
    item = atendimento.__dict__
    item["id"] = entity.id

    return jsonify(item), 201


@bp.route("", methods=["GET"])
def get_all() -> Any:
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    order_by_param = request.args.get("order_by", default="id", type=str)

    atendimento_service = DeliveryService()
    atendimentos = atendimento_service.get_all(page, per_page, order_by_param)

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

@bp.route("/angel_productivity", methods=["GET"])
def get_angel_productivity() -> Any:
    at_most = request.args.get("at_most", default=100, type=int)

    atendimento_service = DeliveryService()
    atendimentos = atendimento_service.get_angel_productivity(at_most=at_most)


    return jsonify(
        {
            "total": len(atendimentos),
            "data": [at for at in atendimentos],
        }
    )

@bp.route("/polo_productivity", methods=["GET"])
def get_polo_productivity() -> Any:
    at_most = request.args.get("at_most", default=100, type=int)

    atendimento_service = DeliveryService()
    atendimentos = atendimento_service.get_polo_productivity(at_most=at_most)

    return jsonify(
        {
            "total": len(atendimentos),
            "data": [at for at in atendimentos],
        }
    )


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update(id: int) -> Any:
    data = request.get_json()

    try:
        atendimento = DeliveryDomainUpdate.from_dict(data)
    except Exception as e:
        raise werkzeug.exceptions.BadRequest(str(e))

    # check if any needed field is missing
    if not atendimento.data_limite or not atendimento.data_de_atendimento or not atendimento.status:
        raise werkzeug.exceptions.BadRequest("Missing required fields")

    delivery_service = DeliveryService()

    entity = delivery_service.update(atendimento, id)
    if not entity:
        raise werkzeug.exceptions.NotFound(description="Resource not found")

    item = atendimento.__dict__
    item["id"] = entity.id

    return jsonify(item), 201


@bp.route("/import_csv", methods=["POST"])
def import_csv() -> Any:
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

    task = import_csv_task.delay(file_content)

    return jsonify({"message": "CSV file is being processed", "task_id": task.id}), 202


@bp.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id: str) -> Any:
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        response = {"state": task_result.state, "status": "Pending..."}
    elif task_result.state != "FAILURE":
        response = {
            "state": task_result.state,
            "status": task_result.info.get("status", ""),
            "result": task_result.info.get("result", ""),
        }
    else:
        response = {"state": task_result.state, "status": str(task_result.info)}
    return jsonify(response)
