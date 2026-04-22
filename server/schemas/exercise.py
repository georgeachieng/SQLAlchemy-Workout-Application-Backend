from marshmallow import Schema, ValidationError, fields, post_load, validate, validates_schema

from models import ALLOWED_CATEGORIES

from .workout_exercise import WorkoutExerciseDetailSchema


class ExerciseListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)


class ExerciseDetailSchema(ExerciseListSchema):
    workout_exercises = fields.List(
        fields.Nested(
            WorkoutExerciseDetailSchema(
                only=("id", "reps", "sets", "duration_seconds", "workout")
            )
        ),
        dump_only=True,
    )


class ExerciseCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    @validates_schema
    def validate_exercise(self, data, **_kwargs):
        name = data.get("name")
        if name is not None and not name.strip():
            raise ValidationError("Exercise name cannot be blank.", field_name="name")

        category = data.get("category")
        if category is not None and category.strip().lower() not in ALLOWED_CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(sorted(ALLOWED_CATEGORIES))}.",
                field_name="category",
            )

    @post_load
    def normalize_exercise(self, data, **_kwargs):
        data["name"] = data["name"].strip()
        data["category"] = data["category"].strip().lower()
        return data

