from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import SessionLocal
from src.backend.api import user, exercise, workout, logged_exercise
from src.backend.crud.user import get_all_users, create_user, update_user, delete_user
from src.backend.crud.exercise import get_all_exercises, create_exercise, update_exercise, delete_exercise
from src.backend.crud.workout import get_all_workouts, create_workout, update_workout, delete_workout
from src.backend.crud.logged_exercise import get_logged_exercises_by_workout, log_exercise, delete_logged_exercise
from src.backend.schemas.user import UserResponse, UserCreate
from src.backend.schemas.exercise import ExerciseResponse, ExerciseCreate
from src.backend.schemas.workout import WorkoutResponse, WorkoutCreate
from src.backend.schemas.logged_exercise import LoggedExerciseResponse, LoggedExerciseCreate

app = FastAPI(
    title="Fitness Tracker API",
    description="An open-source API for tracking workouts and recommending fitness plans",
    version="1.0.0"
)

# CORS Middleware -- Adjust this for production security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API routes
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])
app.include_router(workout.router, prefix="/workouts", tags=["Workouts"])
app.include_router(logged_exercise.router, prefix="/logged_exercises", tags=["Logged Exercises"])

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Fitness Tracker API!"}

# /docs endpoint that React is expecting
@app.get("/docs", tags=["Docs"])
def get_docs():
    return {"message": "Hello from the backend!"}

# GET all users
@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# POST create a new user
@app.post("/users", response_model=UserResponse, tags=["Users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.name, user.email)

# PUT update user details
@app.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user.name, user.email)

# DELETE user
@app.delete("/users/{user_id}", tags=["Users"])
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)

# POST create a new exercise
@app.post("/exercises", response_model=ExerciseResponse, tags=["Exercises"])
def create_new_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return create_exercise(db, exercise.name, exercise.body_parts)

# PUT update exercise details
@app.put("/exercises/{exercise_id}", response_model=ExerciseResponse, tags=["Exercises"])
def update_existing_exercise(exercise_id: int, exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return update_exercise(db, exercise_id, exercise.name, exercise.body_parts)

# DELETE exercise
@app.delete("/exercises/{exercise_id}", tags=["Exercises"])
def delete_existing_exercise(exercise_id: int, db: Session = Depends(get_db)):
    return delete_exercise(db, exercise_id)

# POST create a new workout
@app.post("/workouts", response_model=WorkoutResponse, tags=["Workouts"])
def create_new_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    return create_workout(db, workout.user_id, workout.date)

# PUT update workout details
@app.put("/workouts/{workout_id}", response_model=WorkoutResponse, tags=["Workouts"])
def update_existing_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    return update_workout(db, workout_id, workout.date)

# DELETE workout
@app.delete("/workouts/{workout_id}", tags=["Workouts"])
def delete_existing_workout(workout_id: int, db: Session = Depends(get_db)):
    return delete_workout(db, workout_id)

# POST log an exercise in a workout
@app.post("/logged_exercises/{workout_id}", response_model=LoggedExerciseResponse, tags=["Logged Exercises"])
def log_new_exercise(workout_id: int, exercise: LoggedExerciseCreate, db: Session = Depends(get_db)):
    return log_exercise(db, workout_id, exercise.exercise_id, exercise.weight, exercise.sets, exercise.reps)

# DELETE a logged exercise
@app.delete("/logged_exercises/{workout_id}/{exercise_id}", tags=["Logged Exercises"])
def delete_logged_exercise_entry(workout_id: int, exercise_id: int, db: Session = Depends(get_db)):
    return delete_logged_exercise(db, workout_id, exercise_id)
