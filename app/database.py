from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL, logger

# Base class for models
Base = declarative_base()

# Database connection with retry logic
MAX_RETRIES = 5
RETRY_DELAY = 5
for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database connected successfully!")
        break
    except Exception as e:
        logger.error(
            "Attempt %s: Database connection failed. Retrying in %s seconds...",
            attempt,
            RETRY_DELAY,
        )

        sleep(RETRY_DELAY)
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
