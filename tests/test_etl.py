import unittest
from unittest.mock import Mock
from app.etl.pipeline import load_data


class TestEtl(unittest.TestCase):
    def setUp(self):
        self.mock_db_session = Mock()

    def test_import_csv_success(self):
        # mock valid CSV data
        result = load_data(
            "tests/test_data/sample_data.csv", self.mock_db_session, chunk_size=100
        )

        # assert accepted rows
        self.assertGreater(result["accepted"], 0)
        self.assertEqual(result["discarded"], 0)

    def test_import_csv_invalid_data(self):
        # mock invalid CSV data
        result = load_data(
            "tests/test_data/invalid_data.csv", self.mock_db_session, chunk_size=100
        )

        # assert rejected rows
        self.assertGreater(result["discarded"], 0)


if __name__ == "__main__":
    unittest.main()
