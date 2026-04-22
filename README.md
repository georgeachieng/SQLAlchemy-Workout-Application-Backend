# Workout Tracker Backend API

## Project Description
This project is a Flask backend API for a workout tracking application used by personal trainers. It manages workouts, reusable exercises, and the join records that connect exercises to workouts with reps, sets, and duration data.

The application uses:
- Flask for the API
- SQLAlchemy for models and relationships
- Flask-Migrate for database migrations
- Marshmallow for serialization and request validation

## Installation
1. Install dependencies:
```bash
pipenv install
```

2. Activate the virtual environment:
```bash
pipenv shell
```

3. Move into the server directory:
```bash
cd server
```

4. Initialize migrations the first time only:
```bash
flask --app app db init
```

5. Create a migration:
```bash
flask --app app db migrate -m "initial workout app models"
```

6. Apply the migration:
```bash
flask --app app db upgrade head
```

7. Seed the database:
```bash
python seed.py
```

## Run Instructions
From the `server/` directory:
```bash
flask --app app run --port 5555
```

## API Endpoints

### Workouts
- `GET /workouts`
  Returns all workouts.

- `GET /workouts/<id>`
  Returns one workout with its associated exercises and workout exercise details.

- `POST /workouts`
  Creates a new workout.

- `DELETE /workouts/<id>`
  Deletes a workout and its associated join records.

### Exercises
- `GET /exercises`
  Returns all exercises.

- `GET /exercises/<id>`
  Returns one exercise with its associated workouts.

- `POST /exercises`
  Creates a new exercise.

- `DELETE /exercises/<id>`
  Deletes an exercise and its associated join records.

### Workout Exercises
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
  Adds an exercise to a workout with `reps`, `sets`, and/or `duration_seconds`.

## Example Request Bodies

### Create a workout
```json
{
  "date": "2026-04-22",
  "duration_minutes": 45,
  "notes": "Upper body strength session"
}
```

### Create an exercise
```json
{
  "name": "Push Up",
  "category": "strength",
  "equipment_needed": false
}
```

### Add an exercise to a workout
```json
{
  "sets": 4,
  "reps": 12
}
```

## Validations Included
- Database constraints:
  - unique exercise `name + category`
  - positive workout duration
  - unique exercise per workout in the join table
  - non-negative reps, sets, and duration values
  - at least one metric present on a workout exercise

- Model validations:
  - exercise names cannot be blank and must be at least 2 characters
  - exercise categories must be from an approved list
  - workout dates cannot be in the future
  - workout notes have a maximum length
  - workout exercise sets and reps must make sense together

- Schema validations:
  - request payloads reject blank or malformed values
  - workout exercise payload requires at least one of `reps`, `sets`, or `duration_seconds`
  - `sets` and `reps` must be sent together for rep-based exercises

## Suggested Test Flow
1. Create exercises.
2. Create workouts.
3. Attach exercises to workouts through the workout exercise endpoint.
4. Retrieve individual workouts and exercises to verify nested serialization.
5. Try invalid payloads to confirm validations are enforced.

## Endpoint Testing Record
The endpoints below are being tested manually with `curl` while the Flask server is running on `http://127.0.0.1:5555`.

Start the API from the `server/` directory:
```bash
flask --app app run --port 5555
```

### 1. Test `GET /workouts`
Purpose: confirm the route responds successfully and returns the workout list in descending date order.

Request:
```bash
curl -i http://127.0.0.1:5555/workouts
```

What to verify:
- response status is `200 OK`
- response body is a JSON array
- each workout includes `id`, `date`, `duration_minutes`, and `notes`

### 2. Test `POST /workouts`
Purpose: confirm a workout can be created and the saved record is returned.

Valid request:
```bash
curl -i -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-22",
    "duration_minutes": 45,
    "notes": "Upper body strength session"
  }'
```

What to verify:
- response status is `201 Created`
- response body includes the new `id`
- returned JSON includes `date`, `duration_minutes`, `notes`, and `workout_exercises`
- `workout_exercises` is returned as an empty array for a new workout

Validation check:
```bash
curl -i -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2099-01-01",
    "duration_minutes": 45,
    "notes": "Future workout"
  }'
```

Expected result:
- response status is `400 Bad Request`
- response body contains a validation error for `date`

### 3. Test `POST /exercises`
Purpose: confirm an exercise can be created and normalized correctly.

Valid request:
```bash
curl -i -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Push Up",
    "category": "strength",
    "equipment_needed": false
  }'
```

What to verify:
- response status is `201 Created`
- response body includes the new `id`
- returned JSON includes `name`, `category`, `equipment_needed`, and `workout_exercises`
- `category` is stored in lowercase

Validation check:
```bash
curl -i -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": " ",
    "category": "strength",
    "equipment_needed": false
  }'
```

Expected result:
- response status is `400 Bad Request`
- response body contains a validation error for `name`

## Project Structure
```text
.
├── Pipfile
├── README.md
└── server
    ├── app.py
    ├── models.py
    ├── schemas.py
    └── seed.py
```
