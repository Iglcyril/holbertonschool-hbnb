import unittest
import json
import uuid
from app import create_app


class TestHBnBEndpoints(unittest.TestCase):
    """Test suite for HBNB API endpoints"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        # Generate unique email for each test
        unique_id = str(uuid.uuid4())[:8]

        # Test data
        self.valid_user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f"jane.doe.{unique_id}@example.com"
        }

        self.invalid_user_data = {
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        }

        self.valid_amenity_data = {
            "name": "Swimming Pool"
        }

        self.invalid_amenity_data = {
            "name": ""
        }

    def test_create_user_valid(self):
        """Test creating a user with valid data"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'],
                         self.valid_user_data['first_name'])
        self.assertEqual(data['last_name'], self.valid_user_data['last_name'])
        self.assertEqual(data['email'], self.valid_user_data['email'])

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.invalid_user_data),
            content_type='application/json'
        )
        # Should return 400 for validation error
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test creating a user with duplicate email"""
        # First user
        self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )

        # Second user with same email
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Email already registered', data.get('error', ''))

    def test_get_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by ID"""
        # First create a user
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "first_name": "Test",
                "last_name": "User",
                "email": "test.user@example.com"
            }),
            content_type='application/json'
        )

        user_data = json.loads(response.data)
        user_id = user_data['id']

        # Get the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertIn('User not found', data.get('error', ''))

    def test_create_amenity_valid(self):
        """Test creating an amenity with valid data"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.valid_amenity_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], self.valid_amenity_data['name'])

    def test_create_amenity_invalid(self):
        """Test creating an amenity with invalid data"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.invalid_amenity_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_valid(self):
        """Test creating a place with valid data"""
        # First create a user and amenity
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "first_name": "Owner",
                "last_name": "Test",
                "email": "owner@example.com"
            }),
            content_type='application/json'
        )
        user_data = json.loads(user_response.data)
        user_id = user_data['id']

        amenity_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({"name": "Air Conditioning"}),
            content_type='application/json'
        )
        amenity_data = json.loads(amenity_response.data)
        amenity_id = amenity_data['id']

        # Create the place
        place_data = {
            "title": "Test Place",
            "description": "A nice test place",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id,
            "amenities": [amenity_id]
        }

        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], place_data['title'])
        self.assertEqual(data['price'], place_data['price'])

    def test_create_place_invalid_coordinates(self):
        """Test creating a place with invalid coordinates"""
        # First create a user
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "first_name": "Owner",
                "last_name": "Test",
                "email": "owner2@example.com"
            }),
            content_type='application/json'
        )
        user_data = json.loads(user_response.data)
        user_id = user_data['id']

        # Try to create place with invalid coordinates
        place_data = {
            "title": "Invalid Place",
            "price": 100.0,
            "latitude": 200,  # Invalid latitude
            "longitude": -500,  # Invalid longitude
            "owner_id": user_id,
            "amenities": []
        }

        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_valid(self):
        """Test creating a review with valid data"""
        # Create user, amenity, and place first
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "first_name": "Reviewer",
                "last_name": "Test",
                "email": "reviewer@example.com"
            }),
            content_type='application/json'
        )
        user_data = json.loads(user_response.data)
        user_id = user_data['id']

        amenity_response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({"name": "Parking"}),
            content_type='application/json'
        )
        amenity_data = json.loads(amenity_response.data)
        amenity_id = amenity_data['id']

        place_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                "title": "Review Test Place",
                "price": 80.0,
                "latitude": 51.5074,
                "longitude": -0.1278,
                "owner_id": user_id,
                "amenities": [amenity_id]
            }),
            content_type='application/json'
        )
        place_data = json.loads(place_response.data)
        place_id = place_data['id']

        # Create the review
        review_data = {
            "text": "Excellent stay, highly recommended!",
            "rating": 4,
            "user_id": user_id,
            "place_id": place_id
        }

        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], review_data['rating'])

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating"""
        # Create necessary entities first
        user_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                "first_name": "Bad",
                "last_name": "Reviewer",
                "email": "bad.reviewer@example.com"
            }),
            content_type='application/json'
        )
        user_data = json.loads(user_response.data)
        user_id = user_data['id']

        # Try to create review with invalid rating
        review_data = {
            "text": "Some review text",
            "rating": 10,  # Invalid rating (should be 1-5)
            "user_id": user_id,
            "place_id": "fake-place-id"  # This will also be invalid
        }

        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps(review_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
