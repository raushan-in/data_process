import unittest
from http import HTTPStatus
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models import GeolocationRecord


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.routes.get_db")
    def test_geolocation_api_success(self, mock_get_db):
        """
        Test the geolocation lookup endpoint for a valid IP address.
        """
        # Mock the database session and query
        mock_db_session = mock_get_db.return_value
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
            GeolocationRecord(
                ip_address="85.175.199.150",
                country_code="US",
                country="United States",
                city="New York",
                latitude=40.7128,
                longitude=-74.0060,
            )
        )
        response = self.client.get("/geolocation/85.175.199.150")

        # success api call
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("app.routes.get_db")
    def test_geolocation_api_data_missing(self, mock_get_db):
        """
        Test the geolocation lookup endpoint for an IP address that does not exist in the database.
        """
        # Mock the database session to return None
        mock_db_session = mock_get_db.return_value
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )

        response = self.client.get("/geolocation/123.123.123.123")

        # assert the response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "ip address not found"})


if __name__ == "__main__":
    unittest.main()
