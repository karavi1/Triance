from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.exercise import ExerciseCreate, ExerciseOut
from src.backend.crud.exercise import create_exercise, get_all_exercises, get_exercise_by_id, delete_exercise

router = APIRouter()

@router.get("/")
def get_exercises(db: Session = Depends(get_db)):
    return get_all_exercises(db)

@router.get("/{exercise_id}")
def get_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/")
def create_new_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return create_exercise(db, exercise)

@router.delete("/{exercise_id}")
def delete_existing_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    success = delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return success