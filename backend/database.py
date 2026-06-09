import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Load the variables from the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Create the SQLAlchemy Engine 
# This handles the low-level connection pool to your Postgres database
engine = create_engine(DATABASE_URL)

# 3. Create a Session Factory
# Every time a user hits an API route, we will spawn a clean session from this factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base Model Class
# Our database tables (models.py) will inherit from this class so SQLAlchemy tracks them
Base = declarative_base()

# 5. Dependency helper function to get the DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()