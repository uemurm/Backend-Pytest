import os
import pytest
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from api_client.base import BaseApiClient

# Load environment variables
load_dotenv()

# --- Database Fixtures ---

@pytest.fixture(scope="session")
def db_engine():
    """Create a SQLAlchemy engine for the test database."""
    # Use the same DB as the app for now (or a separate test DB if preferred)
    database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_db")
    return create_engine(database_url)

@pytest.fixture(scope="function", autouse=True)
def clean_db(db_engine):
    """
    Clean the database before each test.
    This ensures test isolation even when running against a real DB.
    """
    # Connect to the DB and truncate the table
    with db_engine.connect() as connection:
        # Use TRUNCATE for faster cleanup than DELETE
        # RESTART IDENTITY resets the auto-increment counter (if used)
        connection.execute(text("TRUNCATE TABLE todos RESTART IDENTITY CASCADE;"))
        connection.commit()

# --- API Client Fixtures ---

@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()

@pytest.fixture(scope="session")
def todo_client(session: requests.Session) -> BaseApiClient:
    """A client for a Todo app running on localhost"""
    base_url = os.getenv('TODO_API_URL', 'http://127.0.0.1:8000')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=5)

@pytest.fixture(scope="session")
def httpbin_client(session: requests.Session) -> BaseApiClient:
    base_url = os.getenv('HTTPBIN_URL', 'https://httpbin.org')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=10)

@pytest.fixture(scope="session")
def dummyjson_client(session: requests.Session) -> BaseApiClient:
    base_url = os.getenv('DUMMYJSON_URL', 'https://dummyjson.com')
    return BaseApiClient(base_url=base_url, session=session, timeout_s=10)

@pytest.fixture(autouse=True)
def debug_on_failure(request, httpbin_client, dummyjson_client, todo_client):
    """
    Print last API request and response if a test fails.
    """
    yield
    
    # Simple debug print (can be enhanced)
    # print("\n[DEBUG] Test Finished")
