from unittest import TestCase, main as unittest_main
from app import app

class ContractorTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
    
    def test_starterpacks_index(self):
        """Test the Starterpacks homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
    
    def test_bag(self):
        """Test the Bag page."""
        result = self.client.get('/bag')
        self.assertEqual(result.status, '200 OK')

if __name__ == '__main__':
    unittest_main()