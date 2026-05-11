import unittest
from app import app, db, User, Property, Inquiry
from flask_login import login_user

class TestRoutesDebug(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.user = User(name="Test User", email="test@example.com", password="password")
        db.session.add(self.user)
        db.session.commit()
        self.prop = Property(title="Test Property", price=100000, location="Test City", user_id=self.user.id)
        db.session.add(self.prop)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_property_detail_debug(self):
        response = self.app.get(f'/property/{self.prop.id}')
        if response.status_code != 200:
            print(f"DETAIL ERROR: {response.data}")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
