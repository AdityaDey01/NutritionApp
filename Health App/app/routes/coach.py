from flask import Blueprint, render_template, request, jsonify
from app.models.ai_engine import get_coach_response

coach_bp = Blueprint("coach", __name__)

@coach_bp.route("/")
def index():
    return render_template("coach.html")

@coach_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = get_coach_response(message)
    return jsonify(response)
