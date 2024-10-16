import unittest

from src.main import app
from src.database.declarative_base import open_session, Base

class BaseTestClass(unittest.TestCase):

    def setUp(self):
        """Set up the test environment"""
        # Create the Flask application with the test configuration
        self.app = app

        # Create a test client
        self.client = self.app.test_client()

        # Establish the app context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Tear down the test environment"""
        # Remove the session and drop all tables
        session = open_session()

        with self.app.app_context():
            # Get all tables
            tables = Base.metadata.sorted_tables
            for table in tables:
                # Execute a delete statement for each table
                session.execute(table.delete())
            session.commit()

        # Pop the app context
        self.app_context.pop()