from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class GeolocationRecord(Base):
    __tablename__ = "geolocation_records"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False, index=True)
    country_code = Column(String, nullable=False)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    extra_data = Column(String, nullable=True)
