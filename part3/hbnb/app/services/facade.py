from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
from app.models.user import User
from datetime import datetime

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        # print("Initialized facade")
    # ===== USER METHODS =====

    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
        )

        user.hash_password(user_data['password'])

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        return user

    # ===== PLACE METHODS =====

    def create_place(self, place_data):
        amenity_ids = place_data.pop("amenities", [])

        print("USER REPO CONTENT:", self.user_repo.get_all())
        print("SEARCHING OWNER:", place_data["owner_id"])

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Invalid owner_id: User does not exist")
        place = Place(**place_data)
        place.owner = owner
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} does not exist")
            amenities.append(amenity)
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place with proper validation"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Validate that place_data is not empty
        if not place_data:
            raise ValueError("No data provided for update")

        # Create a copy of current place data for validation
        current_data = {
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        }

        # Update with new data
        for key, value in place_data.items():
            if key in ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']:
                current_data[key] = value

        # Validate the updated data by creating a temporary Place instance
        try:
            temp_place = Place(
                title=current_data['title'],
                description=current_data['description'], 
                price=current_data['price'],
                latitude=current_data['latitude'],
                longitude=current_data['longitude'],
                owner_id=current_data['owner_id']
            )

            # If validation passed, update the existing place
            place.title = temp_place.title
            place.description = temp_place.description
            place.price = temp_place.price
            place.latitude = temp_place.latitude
            place.longitude = temp_place.longitude
            place.owner_id = temp_place.owner_id
            place.updated_at = datetime.now()

            # Handle amenities if provided
            if 'amenities' in place_data:
                amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        amenities.append(amenity)
                    else:
                        raise ValueError(f"Amenity with ID {amenity_id} not found")
                place.amenities = amenities

        except (ValueError, TypeError) as e:
            # Re-raise validation errors to be caught by API layer
            raise e

        return place
    # ===== REVIEW METHODS =====

    def create_review(self, review_data):
        """Create a new review with validation"""
        from app.models.review import Review

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("Invalid user_id: User does not exist")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Invalid place_id: Place does not exist")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review with validation"""
        from app.models.review import Review

        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Validate that review_data is not empty
        if not review_data:
            raise ValueError("No data provided for update")

        # Create current data with fallbacks
        current_data = {
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place_id,
            'user_id': review.user_id
        }

        # Update with new data
        for key, value in review_data.items():
            if key in ['text', 'rating', 'place_id', 'user_id']:
                current_data[key] = value

        # Validate user_id and place_id exist if being updated
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("Invalid user_id: User does not exist")

        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Invalid place_id: Place does not exist")

        # Validate the updated data by creating a temporary Review instance
        try:
            temp_review = Review(
                text=current_data['text'],
                rating=current_data['rating'],
                place_id=current_data['place_id'],
                user_id=current_data['user_id']
            )

            # If validation passed, update the existing review
            review.text = temp_review.text
            review.rating = temp_review.rating
            review.place_id = temp_review.place_id
            review.user_id = temp_review.user_id
            review.updated_at = datetime.now()

        except (ValueError, TypeError) as e:
            # Re-raise validation errors to be caught by API layer
            raise e

        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False

        return self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [
            review for review in all_reviews if review.place_id == place_id]

    # ===== AMENITY METHODS =====

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            return None

        # Validate that amenity_data is not empty
        if not amenity_data:
            raise ValueError("No data provided for update")

        if 'name' in amenity_data:
            # Validate the new name using Amenity constructor validation
            # This will raise ValueError/TypeError if invalid
            try:
                temp_amenity = Amenity(name=amenity_data['name'])
                # If validation passed, update the existing amenity
                amenity.name = temp_amenity.name  # Use the cleaned name (stripped)
                amenity.updated_at = datetime.now()
            except (ValueError, TypeError) as e:
                # Re-raise the validation error to be caught by API layer
                raise e
        else:
            raise ValueError("Name field is required for amenity update")
        return amenity
