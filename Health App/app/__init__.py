from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nutrismart-ai-hackathon-2026")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../nutrismart.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.recommender import recommender_bp
    from app.routes.tracker import tracker_bp
    from app.routes.habits import habits_bp
    from app.routes.grocery import grocery_bp
    from app.routes.coach import coach_bp
    from app.routes.profile import profile_bp
    from app.routes.insights import insights_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(recommender_bp, url_prefix="/recommender")
    app.register_blueprint(tracker_bp, url_prefix="/tracker")
    app.register_blueprint(habits_bp, url_prefix="/habits")
    app.register_blueprint(grocery_bp, url_prefix="/grocery")
    app.register_blueprint(coach_bp, url_prefix="/coach")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(insights_bp, url_prefix="/insights")

    with app.app_context():
        db.create_all()

    return app
