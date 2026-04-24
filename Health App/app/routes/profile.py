from flask import Blueprint, render_template
from app.models.ai_engine import load_user_profiles

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/")
def index():
    profiles = load_user_profiles()
    user = profiles.get("demo_user", {})
    return render_template("profile.html", user=user)
