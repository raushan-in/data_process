import time
from typing import Dict

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.config import CHUNK_SIZE, logger
from app.database import get_db
from app.etl.validators import validate_chunk
from app.models import GeolocationRecord


def load_data(
    file_path: str, db_session: Session, chunk_size: int
) -> Dict[str, int | float]:
    """
    Loads data from a CSV file into the database in chunks, validating and deduplicating records.

    This function processes a CSV file in chunks, validates the data, and inserts it into the
    `GeolocationRecord` database table. It uses PostgreSQL's `ON CONFLICT DO NOTHING` to handle
    duplicate records based on the `ip_address` column.

    Args:
        file_path (str): Path to the CSV file containing geolocation data.
        db_session (Session): SQLAlchemy database session used for executing queries and transactions.
        chunk_size (int): Number of rows to process in each chunk.

    Returns:
        Dict[str, int | float]: A dictionary containing processing statistics:
            - `accepted` (int): Number of records successfully inserted into the database.
            - `discarded` (int): Number of records discarded due to validation failures.
            - `time_elapsed` (float): Total time taken for the data loading process, in seconds.

    Notes:
        - The CSV file should have the following columns:
          `ip_address`, `country_code`, `country`, `city`, `latitude`, `longitude`, `mystery_value`.
        - Validation is performed using the `validate_geolocation_row` function.
    """

    stats = {"accepted": 0, "discarded": 0}

    logger.info("Starting CSV import from %s", file_path)

    chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

    for i, chunk in enumerate(chunk_iter, start=1):
        print(f"Processing chunk #{i}...")

        # Validate and transform the chunk
        valid_chunk, discarded_count = validate_chunk(chunk)
        stats["discarded"] += discarded_count

        if not valid_chunk.empty:
            # Insert valid rows into the database
            records_to_insert = valid_chunk.to_dict(orient="records")
            stmt = insert(GeolocationRecord).values(records_to_insert)
            stmt = stmt.on_conflict_do_nothing(index_elements=["ip_address"])
            db_session.execute(stmt)
            db_session.commit()

            stats["accepted"] += len(records_to_insert)
    
    return stats


def start():
    """
    Start the ETL process. \n
    - Read data from sample CSV file
    - Clean the data
    - Load data into app database
    - Print pipeline statistics
    """
    sample_file_path = "app/etl/data/data_dump.csv"  # To read given sample data
    db_session = next(get_db())
    stats = load_data(
        file_path=sample_file_path, db_session=db_session, chunk_size=CHUNK_SIZE
    )
    logger.info(
        "CSV import completed. \n Accepted: %d, Discarded: %d, Time elapsed: %.2f seconds",
        stats["accepted"],
        stats["discarded"],
        stats["time_elapsed"],
    )
    logger.info("***** END ******")


if __name__ == "__main__":
    start()
