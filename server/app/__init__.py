from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db

migrate = Migrate()


def error_response(message, status_code=400):
    return make_response(jsonify({"error": message}), status_code)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.exercises import exercises_bp
    from .routes.workout_exercises import workout_exercises_bp
    from .routes.workouts import workouts_bp

    app.register_blueprint(workouts_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(workout_exercises_bp)

    register_error_handlers(app)
    return app


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return make_response(jsonify({"errors": error.messages}), 400)

    @app.errorhandler(404)
    def handle_404(_error):
        return error_response("Resource not found.", 404)

    @app.errorhandler(405)
    def handle_405(_error):
        return error_response("Method not allowed.", 405)


app = create_app()

