from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.logged_exercise import LoggedExerciseCreate, LoggedExerciseOut
from src.backend.crud.logged_exercise import (
    log_exercise,
    get_logged_exercises_by_workout,
    delete_logged_exercise,
)

router = APIRouter()

@router.post("/{workout_id}/log", response_model=LoggedExerciseOut, status_code=status.HTTP_201_CREATED)
def create_logged_exercise(workout_id: UUID, entry: LoggedExerciseCreate, db: Session = Depends(get_db)):
    """
    Log a new exercise entry to a specific workout.
    """
    return log_exercise(db, entry, workout_id)

@router.get("/{workout_id}/entries", response_model=list[LoggedExerciseOut])
def read_logged_exercises_by_workout(workout_id: UUID, db: Session = Depends(get_db)):
    """
    Get all logged exercises for a given workout.
    """
    return get_logged_exercises_by_workout(db, workout_id)

@router.delete("/{workout_id}/entry/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_logged_exercise(workout_id: UUID, exercise_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a logged exercise by workout ID and exercise ID.
    """
    success = delete_logged_exercise(db, workout_id, exercise_id)
    if not success:
        raise HTTPException(status_code=404, detail="Logged exercise not found")
    return None  # FastAPI interprets this as 204