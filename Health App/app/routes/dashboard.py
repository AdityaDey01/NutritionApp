from flask import Blueprint, render_template
from app.models.ai_engine import get_dashboard_data

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    data = get_dashboard_data("demo_user")
    return render_template("dashboard.html", **data)
