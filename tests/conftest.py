from tools.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.database import get_db
from src.models.model import Base
import pytest
from fastapi.testclient import TestClient
from src.main import app

"""-----------------------------DB Operations with SQL Alchemy starts----------------------------------"""

SQLALCHEMY_DATABASE_URL = f"postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.TEST_DATABASE_PORT}/{setting.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("Droping all tables")
    Base.metadata.drop_all(bind=engine)  # It will drop all the tables
    print("Creating all tables")
    Base.metadata.create_all(bind=engine)  # IT will recreate all the tables
    db = TestingSessionLocal()
    try:
        print("Opening the DB session from TestingSessionLocal")
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            print("Yielding the session which was passed into client")
            yield session
        finally:
            session.close()

    # this below command will swap the get_db with override_get_db method
    # when its being called from any method's "db: Session = Depends(get_db)""
    app.dependency_overrides[get_db] = override_get_db
    # yield is same as return but it gives flexiblity to run code after returnng.
    yield TestClient(app)
