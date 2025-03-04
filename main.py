from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.backend.database.configure import SessionLocal, engine, Base  # Import engine & Base

# Import User CRUD & Schemas
from src.backend.models.user import User
from src.backend.crud.user import get_all_users, get_user_by_id, create_user, update_user, delete_user
from src.backend.schemas.user import UserResponse, UserCreate

# Import Exercise CRUD & Schemas
from src.backend.models.exercise import Exercise
from src.backend.crud.exercise import get_all_exercises, get_exercise_by_id, create_exercise, update_exercise, delete_exercise
from src.backend.schemas.exercise import ExerciseResponse, ExerciseCreate, ExerciseUpdate

app = FastAPI(
    title="CFT",
    description="Backend API for fitness tracking",
    version="1.0.0"
)

# Ensure tables are created on startup
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### **USER ROUTES**

@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.name, user.email)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, name=user.name, email=user.email)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

### **EXERCISE ROUTES**

@app.get("/exercises/", response_model=List[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    exercises = get_all_exercises(db)
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found")
    return exercises

@app.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@app.post("/exercises/", response_model=ExerciseResponse)
def create_new_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return create_exercise(db, exercise.name, exercise.body_parts)

@app.put("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_existing_exercise(exercise_id: int, exercise: ExerciseUpdate, db: Session = Depends(get_db)):
    updated_exercise = update_exercise(db, exercise_id, name=exercise.name, body_parts=exercise.body_parts)
    if not updated_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return updated_exercise

@app.delete("/exercises/{exercise_id}", response_model=ExerciseResponse)
def delete_existing_exercise(exercise_id: int, db: Session = Depends(get_db)):
    deleted_exercise = delete_exercise(db, exercise_id)
    if not deleted_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return deleted_exercise
