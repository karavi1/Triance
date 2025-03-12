from sqlalchemy.orm import Session
from src.backend.models.logged_exercise import LoggedExercise

def log_exercise(db: Session, workout_id: int, exercise_id: int, weight: float, sets: int, reps: int):
    """Log an exercise for a workout."""
    log_entry = LoggedExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        weight=weight,
        sets=sets,
        reps=reps
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_logged_exercises_by_workout(db: Session, workout_id: int):
    """Retrieve all logged exercises for a specific workout."""
    return db.query(LoggedExercise).filter(LoggedExercise.workout_id == workout_id).all()

def delete_logged_exercise(db: Session, workout_id: int, exercise_id: int):
    """Delete a specific logged exercise from a workout."""
    log_entry = db.query(LoggedExercise).filter(
        LoggedExercise.workout_id == workout_id,
        LoggedExercise.exercise_id == exercise_id
    ).first()
    if not log_entry:
        return None
    db.delete(log_entry)
    db.commit()
    return True
