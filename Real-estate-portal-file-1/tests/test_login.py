import unittest
from app import app  # Assuming Flask app is imported

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()