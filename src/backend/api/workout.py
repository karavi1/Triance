from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import get_db
from src.backend.schemas.workout import WorkoutCreate, WorkoutResponse
from src.backend.crud.workout import create_workout, get_workout_by_id, get_all_workouts, update_workout, delete_workout

router = APIRouter()

# GET all workouts
@router.get("/", response_model=List[WorkoutResponse])
def get_workouts(db: Session = Depends(get_db)):
    workouts = get_all_workouts(db)
    if not workouts:
        raise HTTPException(status_code=404, detail="No workouts found")
    return workouts

# GET a workout by ID
@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

# POST create a new workout
@router.post("/", response_model=WorkoutResponse)
def create_new_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    return create_workout(db, user_id=workout.user_id, date=workout.date)

# PUT update workout details
@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_existing_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    updated_workout = update_workout(db, workout_id, date=workout.date)
    if not updated_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return updated_workout

# DELETE workout
@router.delete("/{workout_id}", response_model=WorkoutResponse)
def delete_existing_workout(workout_id: int, db: Session = Depends(get_db)):
    deleted_workout = delete_workout(db, workout_id)
    if not deleted_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return deleted_workout