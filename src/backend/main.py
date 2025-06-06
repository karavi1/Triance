from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.database.configure import get_db
from src.backend.api import user, exercise, workout, logged_exercise

app = FastAPI(
    title="Fitness Tracker API",
    description="An open-source API for tracking workouts and visualization",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://3.19.64.107",
        "http://localhost:3000",
        "http://18.191.202.36:8000",
        "https://triance.app",
        "https://www.triance.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(exercise.router, prefix="/api/exercises", tags=["Exercises"])
app.include_router(workout.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(logged_exercise.router, prefix="/api/logged_exercises", tags=["Logged Exercises"])

# Root endpoint
@app.get("/api", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Fitness Tracker API!"}

# /docs endpoint that React is expecting
@app.get("/api/custom-docs", tags=["Docs"])
def get_docs():
    return {"message": "Hello from the backend!"}