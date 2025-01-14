from flask import Blueprint, Response, jsonify, request

bp = Blueprint("base", __name__)


@bp.route("/", methods=["GET"])
def index() -> str:
    return "Hello, World!"


@bp.route("/echo", methods=["GET"])
def echo() -> Response:
    data = request.get_json()

    return jsonify(data)
