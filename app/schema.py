from typing import Optional

from pydantic import BaseModel


class GeolocationResponse(BaseModel):
    ip_address: str
    country_code: str
    country: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True  # for compatibility with SQLAlchemy models
