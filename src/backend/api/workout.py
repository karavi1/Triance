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
def get_workouts(db: Session = Depends(get_db)):
    return get_all_workouts(db)


@router.get("/workout_id/{workout_id}", response_model=WorkoutOut)
def get_workout_by_id(workout_id: UUID, db: Session = Depends(get_db)):
    workout = get_workout_by_workout_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.get("/latest/user/{username}", response_model=WorkoutOut)
def get_latest_workout_by_user(username: str, db: Session = Depends(get_db)):
    workout = get_last_workout(username, db)
    if not workout:
        raise HTTPException(status_code=404, detail="No workouts found for this user")
    return workout


@router.get("/user/{username}", response_model=list[WorkoutOut])
def get_workouts_by_username(username: str, db: Session = Depends(get_db)):
    return get_all_workouts_by_name(username, db)


@router.get("/{username}/latest/{workout_type}", response_model=WorkoutOut)
def get_latest_workout_by_user_and_type(username: str, workout_type: str, db: Session = Depends(get_db)):
    workout = get_last_workout_based_on_username_and_type(username, workout_type, db)
    if not workout:
        raise HTTPException(status_code=404, detail="No workouts of this type found for this user")
    return workout


@router.post("/", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_new_workout(workout: WorkoutCreateSimple, db: Session = Depends(get_db)):
    return create_workout(db, workout)


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_workout(workout_id: UUID, db: Session = Depends(get_db)):
    success = delete_workout(db, workout_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workout not found")
    return None

# Delete all workouts for a certain user (with time period and without)