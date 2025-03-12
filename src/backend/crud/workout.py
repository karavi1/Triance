from sqlalchemy.orm import Session
from src.backend.models.workout import Workout

def create_workout(db: Session, user_id: int, date: str):
    """Create a new workout."""
    workout = Workout(user_id=user_id, date=date)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

def get_workout_by_id(db: Session, workout_id: int):
    """Retrieve a workout by its ID."""
    return db.query(Workout).filter(Workout.id == workout_id).first()

def get_all_workouts(db: Session):
    """Retrieve all workouts."""
    return db.query(Workout).all()

def update_workout(db: Session, workout_id: int, date: str = None):
    """Update a workout's date."""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        return None
    if date:
        workout.date = date
    db.commit()
    db.refresh(workout)
    return workout

def delete_workout(db: Session, workout_id: int):
    """Delete a workout by its ID."""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        return None
    db.delete(workout)
    db.commit()
    return True
