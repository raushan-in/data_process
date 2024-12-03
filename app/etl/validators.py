from typing import Optional
import ipaddress

import pandas as pd

from app.constants import (
    COLUMN_CITY,
    COLUMN_COUNTRY,
    COLUMN_COUNTRY_CODE,
    COLUMN_IP_ADDRESS,
    COLUMN_LATITUDE,
    COLUMN_LONGITUDE,
    COLUMN_MYSTERY_VALUE,
)


def validate_geolocation_row(row: pd.Series) -> Optional[dict]:
    """
    Validates and transforms a geolocation data row into a dictionary format suitable for database insertion.

    This function checks if a given row from the CSV contains the required fields (`ip_address`, `country_code`)
    and ensures the data is clean and properly formatted. If validation succeeds, the row is transformed into a
    dictionary. If any required field is missing or the data is invalid, the function returns `None`.

    Args:
        row (pd.Series): A pandas Series object representing a single row of geolocation data.

    Returns:
        Optional[dict]: A dictionary containing the cleaned and transformed row data if validation succeeds.
        The dictionary has the following structure:
            - `ip_address` (str): Either IPv4 or IPv6 IP addresses.
            - `country_code` (str): The country code.
            - `country` (Optional[str]): The country name, or `None` if missing.
            - `city` (Optional[str]): The city name, or `None` if missing or empty.
            - `latitude` (Optional[float]): The latitude as a float, or `None` if missing or invalid.
            - `longitude` (Optional[float]): The longitude as a float, or `None` if missing or invalid.
            - `extra_data` (Any): Additional data from the `MYSTERY_VALUE` field.
        Returns `None` if the row is invalid.

    Raises:
        ValueError: If data in a field (e.g., latitude or longitude) cannot be converted to the expected type.
        AttributeError: If expected fields are missing or improperly formatted.

    Notes:
        - Rows with missing or null `ip_address` or `country_code` are considered invalid.
        - Latitude and longitude values are converted to floats if valid; otherwise, they default to `None`.
    """

    required_fields = [COLUMN_IP_ADDRESS, COLUMN_COUNTRY_CODE]
    for field in required_fields:
        if not row.get(field):
            return None

    try:
        return {
            "ip_address": str(ipaddress.ip_address(row[COLUMN_IP_ADDRESS].strip())),
            "country_code": row[COLUMN_COUNTRY_CODE].strip(),
            "country": row.get(COLUMN_COUNTRY, "").strip(),
            "city": row.get(COLUMN_CITY, "").strip() or None,
            "latitude": (
                float(row[COLUMN_LATITUDE])
                if is_valid_float(row[COLUMN_LATITUDE])
                else None
            ),
            "longitude": (
                float(row[COLUMN_LONGITUDE])
                if is_valid_float(row[COLUMN_LONGITUDE])
                else None
            ),
            "extra_data": row[COLUMN_MYSTERY_VALUE],
        }
    except (ValueError, AttributeError):
        return None


def is_valid_float(value) -> bool:
    """
    Checks if a value can be safely converted to a float.

    Args:
        value: The value to check.

    Returns:
        bool: True if the value is a valid float, False otherwise.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
