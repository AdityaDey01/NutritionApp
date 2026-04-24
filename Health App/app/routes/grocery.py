from flask import Blueprint, render_template, request, jsonify
from app.models.ai_engine import get_meal_plan

grocery_bp = Blueprint("grocery", __name__)

@grocery_bp.route("/")
def index():
    diet = request.args.get("diet", "balanced")
    plan_data = get_meal_plan(diet)
    return render_template("grocery.html", **plan_data, selected_diet=diet)

@grocery_bp.route("/plan")
def get_plan():
    diet = request.args.get("diet", "balanced")
    return jsonify(get_meal_plan(diet))
