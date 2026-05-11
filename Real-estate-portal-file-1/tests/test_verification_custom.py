import unittest
from app import app, db, User, Property, Inquiry, Review
from flask_login import login_user
from datetime import datetime

class TestVerification(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test users
        self.user1 = User(name="User Only", email="user@test.com", password="password")
        self.owner = User(name="Owner", email="owner@test.com", password="password")
        db.session.add(self.user1)
        db.session.add(self.owner)
        db.session.commit()

        # Create test property
        self.prop = Property(
            title="Test Property",
            price=100000,
            location="TestCity",
            address="123 Test St",
            property_type="house",
            bedrooms=3,
            bathrooms=2,
            area=1500,
            amenities="pool,garage",
            user_id=self.owner.id
        )
        db.session.add(self.prop)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, user):
        with self.app.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True

    def test_dashboard_inquiries(self):
        # Create an inquiry for the owner
        inquiry = Inquiry(
            sender_id=self.user1.id,
            receiver_id=self.owner.id,
            property_id=self.prop.id,
            message="Interested!",
            date_sent=datetime.utcnow()
        )
        db.session.add(inquiry)
        db.session.commit()

        # Login as owner
        self.login(self.owner)
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Interested!", response.data)
        self.assertIn(b"Inbox", response.data)

    def test_property_detail_and_review(self):
        self.login(self.user1)
        
        # Test Detail Page
        response = self.app.get(f'/property/{self.prop.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Property", response.data)
        self.assertIn(b"123 Test St", response.data)

        # Test Add Review
        response = self.app.post(f'/add-review/{self.prop.id}', data={
            'rating': 5,
            'comment': 'Great house!'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify review in DB
        review = Review.query.first()
        self.assertEqual(review.comment, 'Great house!')
        self.assertEqual(review.rating, 5)

    def test_edit_property(self):
        self.login(self.owner)
        response = self.app.post(f'/edit-property/{self.prop.id}', data={
            'title': 'Updated Title',
            'price': 200000,
            'location': 'NewCity',
            'address': '456 New St',
            'property_type': 'apartment',
            'bedrooms': 2,
            'bathrooms': 1,
            'area': 1000,
            'amenities': 'gym'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        updated_prop = Property.query.get(self.prop.id)
        self.assertEqual(updated_prop.title, 'Updated Title')
        self.assertEqual(updated_prop.address, '456 New St')

    def test_search_results(self):
        self.login(self.user1)
        # Search by matching location
        response = self.app.get('/search-results?location=TestCity')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Property", response.data)

        # Search by non-matching location
        response = self.app.get('/search-results?location=OtherCity')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Test Property", response.data)

    def test_contact_seller(self):
        self.login(self.user1)
        response = self.app.post(f'/contact/{self.prop.id}', data={
            'message': 'Hello owner'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Check Inquiry created
        inquiry = Inquiry.query.filter_by(message='Hello owner').first()
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry.receiver_id, self.owner.id)

if __name__ == '__main__':
    unittest.main()
