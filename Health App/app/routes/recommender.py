from flask import Blueprint, render_template, request, jsonify
from app.models.ai_engine import get_recommendations, get_mood_suggestions, get_weather_suggestions, load_food_db, calculate_food_score

recommender_bp = Blueprint("recommender", __name__)

@recommender_bp.route("/")
def index():
    return render_template("recommender.html")

@recommender_bp.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    results = get_recommendations(
        meal_query=data.get("meal_query", ""),
        diet_pref=data.get("diet_pref", "any"),
        health_goal=data.get("health_goal", "balanced"),
        budget=data.get("budget", "medium"),
        meal_time=data.get("meal_time", "lunch"),
        stress_level=data.get("stress_level", "normal"),
        workout_day=data.get("workout_day", False)
    )
    return jsonify(results)

@recommender_bp.route("/mood", methods=["POST"])
def mood():
    data = request.get_json()
    suggestions = get_mood_suggestions(data.get("mood", "happy"))
    return jsonify({"suggestions": suggestions})

@recommender_bp.route("/weather", methods=["POST"])
def weather():
    data = request.get_json()
    suggestions = get_weather_suggestions(data.get("weather", "sunny"))
    return jsonify({"suggestions": suggestions})

@recommender_bp.route("/score", methods=["POST"])
def score_food():
    data = request.get_json()
    db = load_food_db()
    food = next((f for f in db["foods"] if f["id"] == data.get("food_id")), None)
    if food:
        score = calculate_food_score(food)
        return jsonify({"food": food, "score": score})
    return jsonify({"error": "Food not found"}), 404

@recommender_bp.route("/scan", methods=["POST"])
def scan_meal():
    """Mock AI scan endpoint."""
    meal_name = request.get_json().get("meal_name", "Unknown Meal")
    db = load_food_db()
    import random
    food = random.choice(db["foods"])
    score = calculate_food_score(food)
    return jsonify({
        "detected": meal_name,
        "matched": food["name"],
        "confidence": round(random.uniform(0.72, 0.97), 2),
        "nutrition": food,
        "score": score
    })
