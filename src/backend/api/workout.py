from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.backend.database.configure import get_db
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutOut
from src.backend.crud.workout import (
    create_workout,
    get_workout_by_workout_id,
    get_all_workouts,
    delete_workout,
    get_last_workout,
    get_last_workout_based_on_username_and_type,
    get_all_workouts_by_name,
)

router = APIRouter()

@router.get("/", response_model=list[WorkoutOut])
def get_all_workouts_handler(db: Session = Depends(get_db)):
    """
    Get all workouts in the system.
    """
    return get_all_workouts(db)

@router.get("/{workout_id}", response_model=WorkoutOut)
def get_workout_by_id_handler(workout_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific workout by its ID.
    """
    workout = get_workout_by_workout_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.get("/user/{username}", response_model=list[WorkoutOut])
def get_workouts_by_user_handler(username: str, db: Session = Depends(get_db)):
    """
    Get all workouts for a given user.
    """
    return get_all_workouts_by_name(username, db)

@router.get("/user/{username}/latest", response_model=WorkoutOut)
def get_latest_workout_by_user_handler(username: str, db: Session = Depends(get_db)):
    """
    Get the most recent workout for a user.
    """
    workout = get_last_workout(username, db)
    if not workout:
        raise HTTPException(status_code=404, detail="No workouts found for this user")
    return workout

@router.get("/user/{username}/latest/{workout_type}", response_model=WorkoutOut)
def get_latest_workout_by_type_handler(username: str, workout_type: str, db: Session = Depends(get_db)):
    """
    Get the most recent workout of a specific type for a user.
    """
    workout = get_last_workout_based_on_username_and_type(username, workout_type, db)
    if not workout:
        raise HTTPException(status_code=404, detail="No workouts of this type found for this user")
    return workout

@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout_handler(workout: WorkoutCreateSimple, db: Session = Depends(get_db)):
    """
    Create a new workout with user and logged exercises.
    """
    return create_workout(db, workout)

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_handler(workout_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a workout by ID.
    """
    success = delete_workout(db, workout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workout not found")
    return None