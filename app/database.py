from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL, logger

# Base class for models
Base = declarative_base()

# Database connection with retry logic
max_retries = 10
retry_delay = 5
for attempt in range(1, max_retries + 1):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database connected successfully!")
        break
    except Exception as e:
        logger.error(
            f"Attempt {attempt}: Database connection failed. Retrying in {retry_delay} seconds..."
        )
        sleep(retry_delay)
else:
    raise ConnectionError("Failed to connect to the database after multiple retries.")


# Dependency to provide a database session
def get_db():
    """
    Yields a database session.
    Automatically closes the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the database
def initialize_database():
    """
    Initializes the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)
