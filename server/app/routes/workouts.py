from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from app import error_response
from models import Workout, db
from schemas import workout_create_schema, workout_detail_schema, workout_list_schema

workouts_bp = Blueprint("workouts", __name__)


@workouts_bp.get("/workouts")
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc(), Workout.id.desc()).all()
    return make_response(jsonify(workout_list_schema.dump(workouts)), 200)


@workouts_bp.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)


@workouts_bp.post("/workouts")
def create_workout():
    data = workout_create_schema.load(request.get_json() or {})
    workout = Workout(**data)
    db.session.add(workout)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response("Unable to create workout because of a database constraint.", 400)
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    return make_response(jsonify(workout_detail_schema.dump(workout)), 201)


@workouts_bp.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)

