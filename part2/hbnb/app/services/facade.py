from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from datetime import datetime


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        # print("Initialized facade")
    # ===== USER METHODS =====

    def create_user(self, user_data):
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
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, value)
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
        from datetime import datetime

        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("Invalid user_id: User does not exist")

        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Invalid place_id: Place does not exist")

        self.review_repo.update(review_id, review_data)

        updated_review = self.review_repo.get(review_id)

        return updated_review

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
