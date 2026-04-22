from datetime import date

from marshmallow import Schema, ValidationError, fields, post_load, validate, validates_schema

from models import ALLOWED_CATEGORIES


class ExerciseListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)


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


class WorkoutListSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)


class WorkoutDetailSchema(WorkoutListSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseDetailSchema(only=("id", "reps", "sets", "duration_seconds", "exercise"))),
        dump_only=True,
    )


class ExerciseDetailSchema(ExerciseListSchema):
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseDetailSchema(only=("id", "reps", "sets", "duration_seconds", "workout"))),
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


workout_list_schema = WorkoutListSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_create_schema = WorkoutCreateSchema()

exercise_list_schema = ExerciseListSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
exercise_create_schema = ExerciseCreateSchema()

workout_exercise_detail_schema = WorkoutExerciseDetailSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()

