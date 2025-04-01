from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.logged_exercise import LoggedExerciseCreate
from src.backend.crud.logged_exercise import log_exercise, get_logged_exercises_by_workout, delete_logged_exercise

router = APIRouter()

@router.post("/{workout_id}/log")
def log_new_exercise(workout_id: UUID, entry: LoggedExerciseCreate, db: Session = Depends(get_db)):
    return log_exercise(db, entry, workout_id)

@router.get("/{workout_id}/entries")
def get_logged_exercises(workout_id: UUID, db: Session = Depends(get_db)):
    return get_logged_exercises_by_workout(db, workout_id)

@router.delete("/{workout_id}/entry/{exercise_id}")
def delete_logged_exercise_entry(workout_id: UUID, exercise_id: UUID, db: Session = Depends(get_db)):
    success = delete_logged_exercise(db, workout_id, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Logged exercise not found")
    return success