from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.backend.database.configure import get_db
from src.backend.models.exercise import Exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseUpdate
from src.backend.crud.exercise import create_exercise, get_all_exercises, get_exercise_by_id, delete_exercise, create_batch_exercise, update_exercise

router = APIRouter()

@router.get("/")
def get_exercises(name: str = None, db: Session = Depends(get_db)):
    exercises = get_all_exercises(db)
    if name:
        exercises = [e for e in exercises if e.name.lower() == name.lower()]
    return exercises

@router.get("/{exercise_id}")
def get_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/")
def create_new_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    existing = db.query(Exercise).filter(Exercise.name == exercise.name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Exercise '{exercise.name}' already exists")
    return create_exercise(db, exercise)

@router.post("/batch/", response_model=List[ExerciseOut])
def create_new_batch_exercise(exercises: List[ExerciseCreate], db: Session = Depends(get_db)):
    return create_batch_exercise(db, exercises)

@router.patch("/")
def update_existing_exercise(exercise_id: UUID, updates: ExerciseUpdate, db: Session = Depends(get_db)):
    updated = update_exercise(db, exercise_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="something bad happened")
    return updated

@router.delete("/{exercise_id}")
def delete_existing_exercise(exercise_id: UUID, db: Session = Depends(get_db)):
    success = delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return success