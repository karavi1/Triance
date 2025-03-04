from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.backend.database.configure import SessionLocal
from src.backend.api import user, exercise

app = FastAPI(
    title="Fitness Tracker API",
    description="An open-source API for tracking workouts and recommending fitness plans",
    version="1.0.0"
)

# CORS Middleware -- Adjust this for production security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include API routes
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Fitness Tracker API!"}
