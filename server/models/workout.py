from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from .db import db


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="check_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    @validates("date")
    def validate_date(self, _key, value):
        if value is None:
            raise ValueError("Workout date is required.")
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value

    @validates("duration_minutes")
    def validate_duration_minutes(self, _key, value):
        if value is None:
            raise ValueError("Workout duration is required.")
        if value <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        if value > 480:
            raise ValueError("Workout duration must be 480 minutes or less.")
        return value

    @validates("notes")
    def validate_notes(self, _key, value):
        if value is not None and len(value.strip()) > 500:
            raise ValueError("Workout notes must be 500 characters or fewer.")
        return value.strip() if isinstance(value, str) else value

