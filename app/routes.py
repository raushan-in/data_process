from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GeolocationRecord
from app.schema import GeolocationResponse

router = APIRouter()


@router.get("/geolocation/{ip_address}", response_model=GeolocationResponse)
def geolocation_lookup(ip_address: str, db: Session = Depends(get_db)):
    """
    Retrieves geolocation details for a given IP address (eg: `85.175.199.150`).
    """
    record = db.query(GeolocationRecord).filter_by(ip_address=ip_address).first()
    if not record:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="ip address not found"
        )
    return record
