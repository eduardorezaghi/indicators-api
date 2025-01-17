from flask import Blueprint, Response, jsonify, request

bp = Blueprint("base", __name__)


@bp.route("/", methods=["GET"])
def index() -> str: # pragma: no cover
    return "Hello, World!"


@bp.route("/echo", methods=["GET"])
def echo() -> Response: # pragma: no cover
    data = request.get_json()

    return jsonify(data)
