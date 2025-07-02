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

def get_exercise_by_id(db: Session, exercise_id: UUID):
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

def get_all_exercises(db: Session):
    return db.query(Exercise).all()

def get_all_exercises_categorized(db: Session):
    exercises = db.query(Exercise).all()
    grouped = defaultdict(list)
    for exercise in exercises:
        if exercise.category:
            grouped[exercise.category.value].append(exercise)
        else:
            grouped["Uncategorized"].append(exercise)
    return grouped

def update_exercise(db: Session, exercise_id: UUID, updates: ExerciseUpdate):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)
    db.commit()
    db.refresh(exercise)
    return exercise

def delete_exercise(db: Session, exercise_id: UUID):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        return False
    db.delete(exercise)
    db.commit()
    return True