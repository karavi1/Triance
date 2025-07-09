from collections import defaultdict
from fastapi import Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Annotated
from src.backend.models.auth_user import AuthUser
from src.backend.models.exercise import Exercise
from src.backend.schemas.exercise import ExerciseCreate, ExerciseUpdate

def create_exercise(db: Session, exercise_data: ExerciseCreate, currentActiveUser: AuthUser):
    exercise = Exercise(
        **exercise_data.model_dump(exclude={"user_id"}),
        user_id=currentActiveUser.id if currentActiveUser else None
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

def create_batch_exercise(db: Session, exercises_data: List[ExerciseCreate], currentActiveUser: AuthUser):
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

def get_exercise_by_id(db: Session, exercise_id: UUID, currentActiveUser: AuthUser):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        # nothing to check ownership on
        return None

    if currentActiveUser and exercise.user_id and exercise.user_id != currentActiveUser.id:
        return None

    return exercise


def get_all_exercises(db: Session, currentActiveUser: AuthUser):
    exercises = db.query(Exercise).all()
    filtered_exercises = []
    for exercise in exercises:
        if currentActiveUser and exercise.user_id and exercise.user_id != currentActiveUser.id:
            continue
        filtered_exercises.append(exercise)
    return filtered_exercises

def get_all_exercises_categorized(db: Session, currentActiveUser: AuthUser):
    exercises = get_all_exercises(db, currentActiveUser)
    grouped = defaultdict(list)
    for exercise in exercises:
        if exercise.category:
            grouped[exercise.category.value].append(exercise)
        else:
            grouped["Uncategorized"].append(exercise)
    return grouped

def update_exercise(db: Session, exercise_id: UUID, updates: ExerciseUpdate, currentActiveUser: AuthUser):
    exercise = get_exercise_by_id(db, exercise_id, currentActiveUser)
    if not exercise:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)
    db.commit()
    db.refresh(exercise)
    return exercise

def delete_exercise(db: Session, exercise_id: UUID, currentActiveUser: AuthUser):
    exercise = get_exercise_by_id(db, exercise_id, currentActiveUser)
    if not exercise:
        return False
    db.delete(exercise)
    db.commit()
    return True