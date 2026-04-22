from .exercise import ExerciseCreateSchema, ExerciseDetailSchema, ExerciseListSchema
from .workout import WorkoutCreateSchema, WorkoutDetailSchema, WorkoutListSchema
from .workout_exercise import (
    WorkoutExerciseCreateSchema,
    WorkoutExerciseDetailSchema,
)

workout_list_schema = WorkoutListSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_create_schema = WorkoutCreateSchema()

exercise_list_schema = ExerciseListSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
exercise_create_schema = ExerciseCreateSchema()

workout_exercise_detail_schema = WorkoutExerciseDetailSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()

__all__ = [
    "ExerciseCreateSchema",
    "ExerciseDetailSchema",
    "ExerciseListSchema",
    "WorkoutCreateSchema",
    "WorkoutDetailSchema",
    "WorkoutListSchema",
    "WorkoutExerciseCreateSchema",
    "WorkoutExerciseDetailSchema",
    "workout_list_schema",
    "workout_detail_schema",
    "workout_create_schema",
    "exercise_list_schema",
    "exercise_detail_schema",
    "exercise_create_schema",
    "workout_exercise_detail_schema",
    "workout_exercise_create_schema",
]

