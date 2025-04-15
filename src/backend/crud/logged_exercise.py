from sqlalchemy.orm import Session
from uuid import UUID
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.schemas.logged_exercise import LoggedExerciseCreate
from src.backend.models.logged_exercise_set import LoggedExerciseSet

def log_exercise(db: Session, log_data: LoggedExerciseCreate, workout_id: UUID):
    logged_sets = [
        LoggedExerciseSet(
            set_number=s.set_number,
            reps=s.reps,
            weight=s.weight
        )
        for s in log_data.sets
    ]

    log_entry = LoggedExercise(
        workout_id=workout_id,
        exercise_id=log_data.exercise_id,
        sets=logged_sets
    )

    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_logged_exercises_by_workout(db: Session, workout_id: UUID):
    return db.query(LoggedExercise).filter(LoggedExercise.workout_id == workout_id).all()

def delete_logged_exercise(db: Session, workout_id: UUID, exercise_id: UUID):
    log_entry = db.query(LoggedExercise).filter(
        LoggedExercise.workout_id == workout_id,
        LoggedExercise.exercise_id == exercise_id
    ).first()
    if not log_entry:
        return False
    db.delete(log_entry)
    db.commit()
    return True