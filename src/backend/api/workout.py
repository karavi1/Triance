from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutOut
from src.backend.crud.workout import create_workout, get_workout_by_id, get_all_workouts, delete_workout, get_last_workout

router = APIRouter()

@router.get("/")
def get_workouts(db: Session = Depends(get_db)):
    return get_all_workouts(db)

@router.get("/{workout_id}")
def get_workout(workout_id: UUID, db: Session = Depends(get_db)):
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.get("/latest/{username}")
def get_latest_workout(username: str, db: Session = Depends(get_db)):
    workout = get_last_workout(username, db)
    if not workout:
        return "No workouts"
    return workout

@router.post("/", response_model=WorkoutOut)
def create_new_workout(workout: WorkoutCreateSimple, db: Session = Depends(get_db)):
    return create_workout(db, workout)

@router.delete("/{workout_id}")
def delete_existing_workout(workout_id: UUID, db: Session = Depends(get_db)):
    success = delete_workout(db, workout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workout not found")
    return success