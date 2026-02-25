from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.models.user import User
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

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

        if 'name' in amenity_data:
            updated_amenity = Amenity(name=amenity_data['name'])
            updated_amenity.id = amenity.id
            updated_amenity.created_at = amenity.created_at
            updated_amenity.save()
            self.amenity_repo.update(amenity_id, updated_amenity)
            return updated_amenity
        return amenity

facade = HBnBFacade()