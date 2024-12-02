import time
from typing import Dict

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.config import CHUNK_SIZE, logger
from app.database import get_db
from app.etl.validators import validate_geolocation_row
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
          `ip_address`, `country_code`, `country`, `city`, `latitude`, `longitude`.
        - Records with null or duplicate `ip_address` values are automatically handled by the database.
        - Validation is performed using the `validate_geolocation_row` function.
    """

    stats = {"accepted": 0, "discarded": 0}
    start_time = time.time()

    logger.info("Starting CSV import from %s", file_path)

    chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

    for i, chunk in enumerate(chunk_iter, start=1):
        logger.info("Processing chunk #%d", i)

        chunk = chunk.dropna(subset=["ip_address", "country_code"])
        chunk = chunk.drop_duplicates(subset=["ip_address"])

        records_to_insert = []
        for _, row in chunk.iterrows():
            sanitized = validate_geolocation_row(row)
            if sanitized:
                records_to_insert.append(sanitized)
                stats["accepted"] += 1
            else:
                stats["discarded"] += 1

        if records_to_insert:
            stmt = insert(GeolocationRecord).values(records_to_insert)
            stmt = stmt.on_conflict_do_nothing(index_elements=["ip_address"])
            db_session.execute(stmt)
            db_session.commit()
            logger.info("Inserted %d records from chunk #%d", len(records_to_insert), i)

    stats["time_elapsed"] = time.time() - start_time
    return stats


def start():
    """
    Start the ETL process. \n
    - Read data from sample CSV file
    - Clean the data
    - Load data into app database
    - Print pipeline statistics
    """
    SAMPLE_FILE_PATH = "app/etl/data/data_dump.csv"
    db_session = next(get_db())
    stats = load_data(
        file_path=SAMPLE_FILE_PATH, db_session=db_session, chunk_size=CHUNK_SIZE
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
