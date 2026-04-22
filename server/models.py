from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

ALLOWED_CATEGORIES = {
    "strength",
    "cardio",
    "mobility",
    "flexibility",
    "balance",
    "hiit",
    "core",
}


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


class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint("name", "category", name="uq_exercise_name_category"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, _key, value):
        if value is None:
            raise ValueError("Exercise name is required.")
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return cleaned

    @validates("category")
    def validate_category(self, _key, value):
        if value is None:
            raise ValueError("Exercise category is required.")
        cleaned = value.strip().lower()
        if cleaned not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Exercise category must be one of: {', '.join(sorted(ALLOWED_CATEGORIES))}."
            )
        return cleaned


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

