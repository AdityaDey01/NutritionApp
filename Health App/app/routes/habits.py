from flask import Blueprint, render_template, request, jsonify
from app.models.ai_engine import load_user_profiles

habits_bp = Blueprint("habits", __name__)

@habits_bp.route("/")
def index():
    profiles = load_user_profiles()
    habits = profiles.get("habits", [])
    challenges = profiles.get("challenges", [])
    leaderboard = profiles.get("leaderboard", [])
    user = profiles.get("demo_user", {})
    return render_template("habits.html", habits=habits, challenges=challenges, leaderboard=leaderboard, user=user)

@habits_bp.route("/complete", methods=["POST"])
def complete_habit():
    data = request.get_json()
    habit_id = data.get("habit_id")
    points_earned = 50
    return jsonify({"status": "success", "points_earned": points_earned, "message": "🎉 Habit completed! +50 points"})
