# Geolocation Service

This application imports large geolocation datasets from a CSV file into a PostgreSQL database and provides an API to query the geolocation data by IP address.

## Features

1. **Chunk-Based CSV Import**: Handles large datasets efficiently by processing data in chunks.
2. **Validation**: Ensures only valid rows are imported, skipping duplicates and invalid entries.
3. **Deduplication**: Removes duplicate rows based on the IP address.
4. **PostgreSQL**: Uses a production-grade database.
5. **API**: Provides an endpoint to query geolocation data by IP address.
6. **Containerization**: Uses Docker and Docker Compose for easy setup and deployment.

---

## Application Structure

```
geo_service/
├── app/
│   ├── __init__.py            # Empty file to make app a module
│   ├── config.py              # Application configuration using .env
│   ├── constants.py           # Constants for CSV column names
│   ├── database.py            # Database setup and connection logic
│   ├── models.py              # Database schema for geolocation records
│   ├── services.py            # Business logic for CSV import
│   ├── main.py                # FastAPI app initialization
│   ├── routes.py              # API routes definition
├── etl/
│   └── data_dump.csv          # Given CSV file with geolocation data
│   ├── validators.py          # Validation logic for data sanitization
│   ├── pipeeline.py           # initiate the etl process
├── tests/
│   ├── __init__.py
│   ├── test_data/             # Sample data for testing
│   ├── test_etl.py            # unit test for etl services like data loading
│   ├── test_database.py       # unit test for database
│   ├── test_api.py            # unit test for api
├── .env                       # Environment variables for configuration
├── Dockerfile                 # Dockerfile to containerize the application
├── docker-compose.yml         # Compose file to run app and PostgreSQL together
├── requirements.txt           # Python dependencies with versions
├── README.md                  # Documentation
```

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed
- credentials configured in `.env`, (ref: example.env)

### Installation

1. Build and start the application:
   ```bash
   docker compose up -d
   ```

2. Access the application:
   - Swagger API Docs: `http://localhost:8000/docs`

---

## Importing Data

To import data from a CSV file into the database:

1. Trigger ETL process from container shell:
   ```bash
   docker exec geo-web-app python app/etl/pipeline.py
   ```

---

## Querying Data

1. Query the geolocation data by IP address:
   ```
   GET /geolocation/{ip_address}
   ```

2. Example Response:
   ```json
   {
      "ip_address": "85.175.199.150",
      "country_code": "TW",
      "country": "Saudi Arabia",
      "city": "Deckowtown",
      "latitude": 25.6561924125008,
      "longitude": -163.7348649682793
   }
   ```

---

## DataBase UI

1. pgadmin : `http://localhost:5050`

---

## Testing

To run unit tests:

1. Run unit tests with code coverage report:
   ```bash
   docker exec -it geo-web-app pytest --disable-warnings --cov=app tests/
   ```

---

## Design Choices

1. **PostgreSQL**: Chosen for scalability and production-readiness.
2. **Pandas**: Efficient for large-scale data processing and validation.
3. **FastAPI**: A modern light weight framework for building high-performance APIs with documentation.

---

## Trade-offs
1. **Limited scalability**:
   - With a growing dataset, this approach will struggle because as it is single-threaded, chunk-by-chunk process doesn't fully utilize CPU resources or database concurrency.
2. **Bottleneck for large dataset**:
   - when working with data that exceeds the capacity (dataset cannot fit into memory) of pandas, owe can leverage distributed processing.


## Scope Of Improvements
- Temporarily drop indexes, then recreate them after the load.
- Add caching (e.g., Redis) for frequent queries.
- Use multithreading for concurrent chunk processing.
- Distributed processing tool like pySpark for really large dataset.