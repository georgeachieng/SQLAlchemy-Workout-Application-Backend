from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from app import error_response
from models import Exercise, Workout, WorkoutExercise, db
from schemas import workout_exercise_create_schema, workout_exercise_detail_schema

workout_exercises_bp = Blueprint("workout_exercises", __name__)


@workout_exercises_bp.post(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises"
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    data = workout_exercise_create_schema.load(request.get_json() or {})
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        **data,
    )
    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error_response(
            "Unable to add this exercise to the workout. It may already be attached.",
            400,
        )
    except ValueError as error:
        db.session.rollback()
        return error_response(str(error), 400)

    return make_response(jsonify(workout_exercise_detail_schema.dump(workout_exercise)), 201)

