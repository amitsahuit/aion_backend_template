from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tools.config import setting

# Set up the database URL
DATABASE_URL = f"postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a sessionmaker for the database
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a base class for declarative models
Base = declarative_base()


# Define a function to get a database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
