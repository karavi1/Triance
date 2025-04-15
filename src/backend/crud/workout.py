from http.client import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.backend.models.user import User
from src.backend.models.enums import WorkoutType
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutUpdate
from src.backend.models.logged_exercise_set import LoggedExerciseSet

def create_workout(db: Session, workout_data: WorkoutCreateSimple):
    user = db.query(User).filter(User.username == workout_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    logged_exercises = []
    for entry in workout_data.logged_exercises:
        exercise = db.query(Exercise).filter(Exercise.name == entry.name).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise '{entry.name}' not found")

        # Create set entries
        logged_sets = [
            LoggedExerciseSet(
                set_number=s.set_number,
                reps=s.reps,
                weight=s.weight
            )
            for s in entry.sets
        ]

        logged_exercise = LoggedExercise(
            exercise_id=exercise.id,
            sets=logged_sets
        )
        logged_exercises.append(logged_exercise)

    workout = Workout(
        user_id=user.id,
        notes=workout_data.notes,
        workout_type=workout_data.workout_type,
        logged_exercises=logged_exercises
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout


def get_workout_by_workout_id(db: Session, workout_id: UUID):
    return db.query(Workout).filter(Workout.id == workout_id).first()

def get_last_workout(username: str, db: Session):
    return ( 
        db.query(Workout)
        .join(User, Workout.user_id == User.id)
        .filter(User.username == username)
        .order_by(Workout.created_time.desc())
        .first()
    )

def get_all_workouts_by_name(username: str, db: Session):
    return (
        db.query(Workout)
        .join(User, Workout.user_id == User.id)
        .filter(User.username == username)
        .order_by(Workout.created_time.desc()) # Export this and the one to a different method?
        .all()
    )

def get_last_workout_based_on_username_and_type(username: str, workout_type: str, db: Session):
    return ( 
        db.query(Workout)
        .join(User, Workout.user_id == User.id)
        .filter(User.username == username, Workout.workout_type == WorkoutType(workout_type))
        .order_by(Workout.created_time.desc())
        .first()
    )

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