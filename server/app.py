from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_create_schema,
    exercise_detail_schema,
    exercise_list_schema,
    workout_create_schema,
    workout_detail_schema,
    workout_exercise_create_schema,
    workout_exercise_detail_schema,
    workout_list_schema,
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


def error_response(message, status_code=400):
    return make_response(jsonify({"error": message}), status_code)


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return make_response(jsonify({"errors": error.messages}), 400)


@app.errorhandler(404)
def handle_404(_error):
    return error_response("Resource not found.", 404)


@app.errorhandler(405)
def handle_405(_error):
    return error_response("Method not allowed.", 405)


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc(), Workout.id.desc()).all()
    return make_response(jsonify(workout_list_schema.dump(workouts)), 200)


@app.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)


@app.post("/workouts")
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


@app.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response("", 204)


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name.asc()).all()
    return make_response(jsonify(exercise_list_schema.dump(exercises)), 200)


@app.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.post("/exercises")
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


@app.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
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


if __name__ == "__main__":
    app.run(port=5555, debug=True)

