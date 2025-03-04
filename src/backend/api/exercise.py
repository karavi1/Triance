from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import get_db
from src.backend.schemas.exercise import ExerciseCreate, ExerciseResponse
from src.backend.crud.exercise import create_exercise, get_all_exercises, get_exercise_by_id, update_exercise, delete_exercise

router = APIRouter()

# GET all exercises
@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    exercises = get_all_exercises(db)
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found")
    return exercises

# GET exercise by ID
@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

# POST create a new exercise
@router.post("/", response_model=ExerciseResponse)
def create_new_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return create_exercise(db, exercise.name, exercise.body_parts)

# PUT update exercise details
@router.put("/{exercise_id}", response_model=ExerciseResponse)
def update_existing_exercise(exercise_id: int, exercise: ExerciseCreate, db: Session = Depends(get_db)):
    updated_exercise = update_exercise(db, exercise_id, name=exercise.name, body_parts=exercise.body_parts)
    if not updated_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return updated_exercise

# DELETE exercise
@router.delete("/{exercise_id}", response_model=ExerciseResponse)
def delete_existing_exercise(exercise_id: int, db: Session = Depends(get_db)):
    deleted_exercise = delete_exercise(db, exercise_id)
    if not deleted_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return deleted_exercise
