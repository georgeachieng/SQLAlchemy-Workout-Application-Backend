from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from app import error_response
from models import Exercise, db
from schemas import exercise_create_schema, exercise_detail_schema, exercise_list_schema

exercises_bp = Blueprint("exercises", __name__)


@exercises_bp.get("/exercises")
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name.asc()).all()
    return make_response(jsonify(exercise_list_schema.dump(exercises)), 200)


@exercises_bp.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@exercises_bp.post("/exercises")
def create_exercise():
    data = exercise_create_schema.load(request.get_json() or {})
    exercise = Exercise(**data)
    db.session.add(exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Unable to create exercise. The exercise may already exist in this category.",
            400,
        )
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 201)


@exercises_bp.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)

