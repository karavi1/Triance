from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from src.backend.database.configure import SessionLocal
from src.backend.api import user, exercise
from src.backend.crud.user import get_all_users  # Import the function to get all users
from src.backend.schemas.user import UserResponse  # Import the response model for users

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

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Fitness Tracker API!"}

# /docs endpoint that React is expecting
@app.get("/docs", tags=["Docs"])
def get_docs():
    return {"message": "Hello from the backend!"}

# GET /users endpoint that returns a list of users
@app.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    # Get the list of all users from the database
    users = get_all_users(db)
    
    # If no users are found, raise a 404 error
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users
