from flask import Blueprint, render_template, request, jsonify
from app.models.ai_engine import generate_weekly_journal, get_weekly_insights, load_food_db, calculate_food_score
import json
from datetime import datetime

tracker_bp = Blueprint("tracker", __name__)

@tracker_bp.route("/")
def index():
    journal = generate_weekly_journal()
    insights = get_weekly_insights(journal)
    return render_template("tracker.html", journal=journal, insights=insights)

@tracker_bp.route("/log", methods=["POST"])
def log_meal():
    data = request.get_json()
    meal = data.get("meal", {})
    score = calculate_food_score(meal) if meal else {}
    return jsonify({"status": "logged", "score": score, "message": f"✅ {meal.get('name', 'Meal')} logged successfully!"})

@tracker_bp.route("/search_food")
def search_food():
    q = request.args.get("q", "").lower()
    db = load_food_db()
    results = [f for f in db["foods"] if q in f["name"].lower()][:8]
    return jsonify({"foods": results})
