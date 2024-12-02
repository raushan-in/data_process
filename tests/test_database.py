import unittest
from sqlalchemy.orm import Session

from app.database import get_db, initialize_database


class TestDatabase(unittest.TestCase):
    def test_initialize_database(self):
        # Ensure database tables are created without errors
        initialize_database()

    def test_get_db_session(self):
        # use the get_db dependency to create a session
        db = next(get_db())
        self.assertIsInstance(db, Session)
        db.close()


if __name__ == "__main__":
    unittest.main()
