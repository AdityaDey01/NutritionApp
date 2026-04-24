from flask import Blueprint, render_template
from app.models.ai_engine import generate_weekly_journal, get_weekly_insights, load_user_profiles

insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/")
def index():
    journal = generate_weekly_journal()
    insights = get_weekly_insights(journal)
    profiles = load_user_profiles()
    restaurants = profiles.get("restaurants", [])
    user = profiles.get("demo_user", {})
    return render_template("insights.html", journal=journal, insights=insights, restaurants=restaurants, user=user)
