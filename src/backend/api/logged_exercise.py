from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import get_db
from src.backend.schemas.logged_exercise import LoggedExerciseCreate, LoggedExerciseResponse
from src.backend.crud.logged_exercise import log_exercise, get_logged_exercises_by_workout, delete_logged_exercise

router = APIRouter()

# POST log an exercise within a workout
@router.post("/{workout_id}/log_exercise", response_model=LoggedExerciseResponse)
def log_new_exercise(workout_id: int, exercise: LoggedExerciseCreate, db: Session = Depends(get_db)):
    return log_exercise(db, workout_id, exercise.exercise_id, exercise.weight, exercise.sets, exercise.reps)

# GET logged exercises for a workout
@router.get("/{workout_id}/logged_exercises", response_model=List[LoggedExerciseResponse])
def get_logged_exercises(workout_id: int, db: Session = Depends(get_db)):
    exercises = get_logged_exercises_by_workout(db, workout_id)
    if not exercises:
        raise HTTPException(status_code=404, detail="No logged exercises found")
    return exercises

# DELETE a logged exercise from a workout
@router.delete("/{workout_id}/logged_exercise/{exercise_id}", response_model=LoggedExerciseResponse)
def delete_logged_exercise_entry(workout_id: int, exercise_id: int, db: Session = Depends(get_db)):
    deleted_exercise = delete_logged_exercise(db, workout_id, exercise_id)
    if not deleted_exercise:
        raise HTTPException(status_code=404, detail="Logged exercise not found")
    return deleted_exercise