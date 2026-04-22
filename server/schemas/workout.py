from datetime import date

from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from .workout_exercise import WorkoutExerciseDetailSchema


class WorkoutListSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)


class WorkoutDetailSchema(WorkoutListSchema):
    workout_exercises = fields.List(
        fields.Nested(
            WorkoutExerciseDetailSchema(
                only=("id", "reps", "sets", "duration_seconds", "exercise")
            )
        ),
        dump_only=True,
    )


class WorkoutCreateSchema(Schema):
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=480))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))

    @validates_schema
    def validate_workout(self, data, **_kwargs):
        workout_date = data.get("date")
        if workout_date and workout_date > date.today():
            raise ValidationError("Workout date cannot be in the future.", field_name="date")

        notes = data.get("notes")
        if notes is not None and not notes.strip():
            raise ValidationError("Notes cannot be blank when provided.", field_name="notes")

