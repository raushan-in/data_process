"""
Entry point of the application.
"""

from fastapi import FastAPI

from app.database import initialize_database
from app.routes import router

app = FastAPI(title="Geolocation")
app.include_router(router)


@app.on_event("startup")
def startup_event():
    initialize_database()
