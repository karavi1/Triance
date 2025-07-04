from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Annotated
from src.backend.database.configure import get_db
from src.backend.models.auth_user import AuthUser
from src.backend.models.enums import ExerciseGroup
from src.backend.models.exercise import Exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseUpdate
from src.backend.auth.util import (
    get_current_active_user
)
from src.backend.crud.exercise import (
    create_batch_exercise,
    create_exercise,
    delete_exercise,
    get_all_exercises,
    get_all_exercises_categorized,
    get_exercise_by_id,
    update_exercise,
)

router = APIRouter()

@router.get("/", response_model=List[ExerciseOut])
def get_exercises(name: str = None, db: Session = Depends(get_db)):
    exercises = get_all_exercises(db)
    if name:
        exercises = [e for e in exercises if e.name.lower() == name.lower()]
    return exercises

@router.get("/categorized")
def get_exercises_categorized(db: Session = Depends(get_db)):
    return get_all_exercises_categorized(db)

@router.get("/categories", response_model=List[str])
def get_exercise_categories():
    return [group.value for group in ExerciseGroup]

@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise_by_id_handler(exercise_id: UUID, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/", response_model=ExerciseOut)
def create_exercise_handler(exercise: ExerciseCreate, db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_active_user)):
    existing = db.query(Exercise).filter(Exercise.name == exercise.name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Exercise '{exercise.name}' already exists")
    return create_exercise(db, exercise, current_user)

@router.post("/batch", response_model=List[ExerciseOut])
def create_batch_exercise_handler(exercises: List[ExerciseCreate], db: Session = Depends(get_db), current_user: AuthUser = Depends(get_current_active_user)):
    return create_batch_exercise(db, exercises, current_user)

@router.patch("/{exercise_id}", response_model=ExerciseOut)
def update_exercise_handler(exercise_id: UUID, updates: ExerciseUpdate, db: Session = Depends(get_db)):
    updated = update_exercise(db, exercise_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Exercise not found or not updated")
    return updated

@router.delete("/{exercise_id}")
def delete_exercise_handler(exercise_id: UUID, db: Session = Depends(get_db)):
    success = delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return success