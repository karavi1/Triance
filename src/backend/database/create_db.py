from database.configure import engine, Base
from src.backend.models.user import User  # Import models to register them

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
