from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from .constants import ALLOWED_CATEGORIES
from .db import db


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

