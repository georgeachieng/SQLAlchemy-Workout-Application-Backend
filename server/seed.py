#!/usr/bin/env python3

from datetime import date

from app import app
from models import Exercise, Workout, WorkoutExercise, db


with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Bodyweight Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Front Plank", category="core", equipment_needed=False)
    jump_rope = Exercise(name="Jump Rope", category="cardio", equipment_needed=True)
    hamstring_stretch = Exercise(
        name="Hamstring Stretch",
        category="flexibility",
        equipment_needed=False,
    )

    print("Creating workouts...")
    upper_body = Workout(
        date=date(2026, 4, 20),
        duration_minutes=45,
        notes="Upper body strength circuit with core finisher.",
    )
    conditioning = Workout(
        date=date(2026, 4, 21),
        duration_minutes=35,
        notes="Conditioning session focused on heart rate intervals.",
    )
    recovery = Workout(
        date=date(2026, 4, 22),
        duration_minutes=25,
        notes="Recovery day with light mobility and stretching.",
    )

    db.session.add_all([push_up, squat, plank, jump_rope, hamstring_stretch])
    db.session.add_all([upper_body, conditioning, recovery])
    db.session.flush()

    print("Linking exercises to workouts...")
    db.session.add_all(
        [
            WorkoutExercise(
                workout_id=upper_body.id,
                exercise_id=push_up.id,
                sets=4,
                reps=12,
            ),
            WorkoutExercise(
                workout_id=upper_body.id,
                exercise_id=plank.id,
                duration_seconds=60,
            ),
            WorkoutExercise(
                workout_id=conditioning.id,
                exercise_id=jump_rope.id,
                duration_seconds=180,
            ),
            WorkoutExercise(
                workout_id=conditioning.id,
                exercise_id=squat.id,
                sets=3,
                reps=15,
            ),
            WorkoutExercise(
                workout_id=recovery.id,
                exercise_id=hamstring_stretch.id,
                duration_seconds=90,
            ),
        ]
    )

    db.session.commit()
    print("Database seeded successfully.")
