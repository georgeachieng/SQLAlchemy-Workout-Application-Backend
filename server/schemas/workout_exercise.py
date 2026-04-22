from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class WorkoutExerciseEmbeddedExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseEmbeddedWorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)


class WorkoutExerciseDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(WorkoutExerciseEmbeddedExerciseSchema, dump_only=True)
    workout = fields.Nested(WorkoutExerciseEmbeddedWorkoutSchema, dump_only=True)


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_workout_exercise(self, data, **_kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration_seconds = data.get("duration_seconds")

        if reps is None and sets is None and duration_seconds is None:
            raise ValidationError(
                "At least one of reps, sets, or duration_seconds is required."
            )

        if (reps is None) != (sets is None):
            raise ValidationError(
                "Reps and sets must be provided together for rep-based exercises."
            )

