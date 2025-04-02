from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.database.configure import get_db
from src.backend.api import user, exercise, workout, logged_exercise

app = FastAPI(
    title="Fitness Tracker API",
    description="An open-source API for tracking workouts and visualization",
    version="1.0.0"
)

# CORS Middleware -- Adjust this for production security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include trimmed API routes
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])
app.include_router(workout.router, prefix="/workouts", tags=["Workouts"])
app.include_router(logged_exercise.router, prefix="/logged_exercises", tags=["Logged Exercises"])

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Fitness Tracker API!"}

# /docs endpoint that React is expecting
@app.get("/custom-docs", tags=["Docs"])
def get_docs():
    return {"message": "Hello from the backend!"}
