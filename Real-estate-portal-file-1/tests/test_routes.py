import unittest
from app import app, db, User, Property, Inquiry
from flask_login import login_user

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(name="Test User", email="test@example.com", password="password")
        db.session.add(self.user)
        db.session.commit()

        # Create a test property
        self.prop = Property(title="Test Property", price=100000, location="Test City", user_id=self.user.id)
        db.session.add(self.prop)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        with self.app.session_transaction() as sess:
            sess['_user_id'] = str(self.user.id)
            sess['_fresh'] = True

    def test_property_detail(self):
        response = self.app.get(f'/property/{self.prop.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Property", response.data)

    def test_edit_property(self):
        self.login()
        response = self.app.post(f'/edit-property/{self.prop.id}', data={
            'title': 'Updated Title',
            'price': 150000,
            'location': 'Updated City'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Title", response.data)

    def test_delete_property(self):
        self.login()
        response = self.app.post(f'/delete-property/{self.prop.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Property.query.get(self.prop.id))

    def test_search(self):
        response = self.app.get('/search?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Property", response.data)

    def test_contact_seller(self):
        self.login()
        response = self.app.post(f'/contact/{self.prop.id}', data={
            'message': 'I am interested'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
