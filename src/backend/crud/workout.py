from http.client import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.backend.models.user import User
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.schemas.workout import WorkoutCreateSimple, WorkoutUpdate
from src.backend.schemas.logged_exercise import LoggedExerciseCreate

def create_workout(db: Session, workout_data: WorkoutCreateSimple):
    # 1. Get user by username
    user = db.query(User).filter(User.username == workout_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Create logged_exercises by resolving exercise names
    logged_exercises = []
    for entry in workout_data.logged_exercises:
        exercise = db.query(Exercise).filter(Exercise.name == entry.name).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise '{entry.name}' not found")

        logged_exercise = LoggedExercise(
            exercise_id=exercise.id,
            sets=entry.sets,
            reps=entry.reps,
            weight=entry.weight
        )
        logged_exercises.append(logged_exercise)

    # 3. Create the workout
    workout = Workout(
        user_id=user.id,
        notes=workout_data.notes,
        logged_exercises=logged_exercises
    )

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout

def get_workout_by_id(db: Session, workout_id: UUID):
    return db.query(Workout).filter(Workout.id == workout_id).first()

def get_last_workout(username: str, db: Session):
    return ( 
        db.query(Workout)
        .join(User, Workout.user_id == User.id)
        .filter(User.username == username)
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