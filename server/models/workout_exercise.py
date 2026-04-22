from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from .db import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise_pair"),
        CheckConstraint(
            "reps IS NULL OR reps >= 0",
            name="check_reps_non_negative",
        ),
        CheckConstraint(
            "sets IS NULL OR sets >= 0",
            name="check_sets_non_negative",
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="check_duration_seconds_non_negative",
        ),
        CheckConstraint(
            "(reps IS NOT NULL) OR (sets IS NOT NULL) OR (duration_seconds IS NOT NULL)",
            name="check_workout_exercise_has_metric",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, _key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0 when provided.")
        return value

    @validates("sets")
    def validate_sets(self, _key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0 when provided.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, _key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration in seconds must be greater than 0 when provided.")
        return value

