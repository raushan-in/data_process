"""
Validation Operations
"""
from ipaddress import ip_address
import numpy as np

import pandas as pd
import pycountry

ISO_COUNTRIES_CODE = {country.alpha_2 for country in pycountry.countries}


def validate_chunk(chunk: pd.DataFrame):
    """
    Validates and transforms a chunk of data in a vectorized manner.

    Args:
        chunk (pd.DataFrame): The chunk of data to validate.

    Returns:
        pd.DataFrame: A cleaned and validated DataFrame with only valid rows.
        int: Number of discarded rows.
    """
    # Clean up leading/trailing spaces and replace empty strings with NaN
    chunk = chunk.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    chunk.replace("", np.nan, inplace=True)

    # Validate IP addresses
    chunk["ip_address"] = chunk["ip_address"].apply(is_valid_ip)

    # Validate country codes
    chunk["country_code"] = chunk["country_code"].apply(is_valid_country_code)

    # Validate latitude and longitude
    chunk["latitude"] = pd.to_numeric(chunk["latitude"], errors="coerce")
    chunk["longitude"] = pd.to_numeric(chunk["longitude"], errors="coerce")

    # Mark invalid rows: any row with invalid mandatory fields
    valid_rows = chunk.dropna(subset=["ip_address", "country_code"])

    # Return valid rows and count of discarded rows
    discarded_count = len(chunk) - len(valid_rows)
    return valid_rows, discarded_count


def is_valid_ip(value):
    try:
        return str(ip_address(value.strip())) if isinstance(value, str) else np.nan
    except ValueError:
        return np.nan


def is_valid_country_code(value):
    return value.upper() if value.upper() in ISO_COUNTRIES_CODE else np.nan

