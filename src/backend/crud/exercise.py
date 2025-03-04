from sqlalchemy.orm import Session
from src.backend.models.exercise import Exercise

def create_exercise(db: Session, name: str, body_parts: list):
    body_parts_str = ",".join(body_parts)  # Convert list to comma-separated string
    exercise = Exercise(name=name, body_parts=body_parts_str)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

def get_exercise_by_id(db: Session, exercise_id: int):
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

def get_all_exercises(db: Session):
    return db.query(Exercise).all()

def update_exercise(db: Session, exercise_id: int, name: str = None, body_parts: list = None):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    if name:
        exercise.name = name
    if body_parts:
        exercise.body_parts = ",".join(body_parts)
    db.commit()
    db.refresh(exercise)
    return exercise

def delete_exercise(db: Session, exercise_id: int):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    db.delete(exercise)
    db.commit()
    return exercise
