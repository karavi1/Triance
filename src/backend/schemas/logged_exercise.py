from pydantic import BaseModel

class LoggedExerciseBase(BaseModel):
    exercise_id: int
    weight: float
    sets: int
    reps: int

class LoggedExerciseCreate(LoggedExerciseBase):
    pass

class LoggedExerciseResponse(LoggedExerciseBase):
    workout_id: int
    exercise_id: int

    class Config:
        orm_mode = True
