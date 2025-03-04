from sqlalchemy.orm import Session
from src.backend.models.exercise import Exercise

def create_exercise(db: Session, name: str, body_parts: list):
    """Create a new exercise with a list of body parts."""
    exercise = Exercise(name=name, body_parts=body_parts)  # ✅ Store as list
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

def get_exercise_by_id(db: Session, exercise_id: int):
    """Retrieve an exercise by its ID."""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

def get_all_exercises(db: Session):
    """Retrieve all exercises."""
    return db.query(Exercise).all()

def update_exercise(db: Session, exercise_id: int, name: str = None, body_parts: list = None):
    """Update an exercise's name and/or body parts."""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    if name:
        exercise.name = name
    if body_parts:
        exercise.body_parts = body_parts  # ✅ Store list directly
    db.commit()
    db.refresh(exercise)
    return exercise

def delete_exercise(db: Session, exercise_id: int):
    """Delete an exercise by its ID."""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    db.delete(exercise)
    db.commit()
    return True  # ✅ Return True for successful deletion
