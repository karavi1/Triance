from sqlalchemy.orm import Session
from uuid import UUID
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.schemas.workout import WorkoutCreate, WorkoutUpdate
from src.backend.schemas.logged_exercise import LoggedExerciseCreate

def create_workout(db: Session, workout_data: WorkoutCreate):
    workout = Workout(
        user_id=workout_data.user_id,
        date=workout_data.date or None,
        notes=workout_data.notes
    )
    db.add(workout)
    db.flush()

    for log in workout_data.exercises:
        db.add(LoggedExercise(**log.model_dump(), workout_id=workout.id))

    db.commit()
    db.refresh(workout)
    return workout

def get_workout_by_id(db: Session, workout_id: UUID):
    return db.query(Workout).filter(Workout.id == workout_id).first()

def get_all_workouts(db: Session):
    return db.query(Workout).all()

def update_workout(db: Session, workout_id: UUID, updates: WorkoutUpdate):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(workout, field, value)
    db.commit()
    db.refresh(workout)
    return workout

def delete_workout(db: Session, workout_id: UUID):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        return False
    db.delete(workout)
    db.commit()
    return True