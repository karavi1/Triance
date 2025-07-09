from collections import defaultdict
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from src.backend.models.auth_user import AuthUser
from src.backend.models.exercise import Exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseUpdate


def create_exercise(db: Session, exercise_data: ExerciseCreate, currentActiveUser: Optional[AuthUser]):
    exercise = Exercise(
        **exercise_data.model_dump(exclude={"user_id"}),
        user_id=currentActiveUser.id if currentActiveUser else None
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def create_batch_exercise(db: Session, exercises_data: List[ExerciseCreate], currentActiveUser: Optional[AuthUser]):
    exercises_list = []
    for exercise_data in exercises_data:
        existing = db.query(Exercise).filter(Exercise.name == exercise_data.name).first()
        if existing:
            continue
        exercise = Exercise(
            **exercise_data.model_dump(exclude={"user_id"}),
            user_id=currentActiveUser.id if currentActiveUser else None
        )
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        exercises_list.append(exercise)

    return exercises_list


def get_exercise_by_id(db: Session, exercise_id: UUID, currentActiveUser: Optional[AuthUser]):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None

    # Allow access if global, owned, or admin
    if exercise.user_id is not None:
        if not currentActiveUser:
            return None
        if not is_exercise_owned_by_user(exercise, currentActiveUser) and not currentActiveUser.is_admin:
            return None

    return exercise


def get_all_exercises(db: Session, currentActiveUser: Optional[AuthUser]):
    # Admin sees everything
    if currentActiveUser and currentActiveUser.is_admin:
        return db.query(Exercise).all()

    exercises = db.query(Exercise).all()
    filtered_exercises = []
    for exercise in exercises:
        if exercise.user_id is None:
            filtered_exercises.append(exercise)
        elif currentActiveUser and exercise.user_id == currentActiveUser.id:
            filtered_exercises.append(exercise)
    return filtered_exercises


def get_all_exercises_categorized(db: Session, currentActiveUser: Optional[AuthUser]):
    exercises = get_all_exercises(db, currentActiveUser)
    grouped = defaultdict(list)
    for exercise in exercises:
        if exercise.category:
            grouped[exercise.category.value].append(exercise)
        else:
            grouped["Uncategorized"].append(exercise)
    return grouped


def update_exercise(db: Session, exercise_id: UUID, updates: ExerciseUpdate, currentActiveUser: AuthUser):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None

    # Only admin or owner can update
    if not currentActiveUser.is_admin and not is_exercise_owned_by_user(exercise, currentActiveUser):
        return None

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)

    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise_id: UUID, currentActiveUser: AuthUser):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return False

    # Only admin or owner can delete
    if not currentActiveUser.is_admin and not is_exercise_owned_by_user(exercise, currentActiveUser):
        return False

    db.delete(exercise)
    db.commit()
    return True


def is_exercise_owned_by_user(exercise: Exercise, user: AuthUser) -> bool:
    return exercise.user_id == user.id