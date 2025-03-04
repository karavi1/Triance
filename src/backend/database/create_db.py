from database.configure import engine, Base
from src.backend.models.user import User
from src.backend.models.exercise import Exercise

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
