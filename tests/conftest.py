import os

# Mock environment variables
os.environ["DB_USER"] = "user"
os.environ["DB_PASSWORD"] = "password"
os.environ["DB_NAME"] = "geolocation"
os.environ["DATABASE_URL"] = "postgresql://user:password@localhost:5432/geolocation"
