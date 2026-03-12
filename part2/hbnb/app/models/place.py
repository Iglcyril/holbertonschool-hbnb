from .BaseModel import BaseModel


class Place(BaseModel):
    """Place model for rental properties"""

    def __init__(
            self, title, price, latitude, longitude, owner_id, description=''):
        """Initialize a new Place instance
        
        Args:
            title: Title of the place
            price: Price per night
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            owner_id: ID of the place owner
            description: Optional description of the place
        """
        super().__init__()

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title must be a non-empty string")
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters")

        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be positive")

        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")

        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")

        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("Owner ID must be a non-empty string")

        # Validation de la description
        if description and not isinstance(description, str):
            raise ValueError("Description must be a string")
        if description and len(description.strip()) > 500:
            raise ValueError("Description must not exceed 500 characters")

        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id.strip()
        self.reviews = []
        self.amenity_ids = []

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity_id):
        """Add an amenity to the place"""
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)

    def update_description(self, new_description):
        """Update the place description
        
        Args:
            new_description: New description text
        
        Raises:
            ValueError: If description is invalid
        """
        if new_description and not isinstance(new_description, str):
            raise ValueError("Description must be a string")
        if new_description and len(new_description.strip()) > 500:
            raise ValueError("Description must not exceed 500 characters")
        
        self.description = new_description.strip() if new_description else ""

    def __str__(self):
        """String representation of the Place object"""
        return f"[Place] ({self.id}) {self.title}"

    def to_dict(self):
        """Convert Place object to dictionary format"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "reviews": [r.id if hasattr(r, 'id') else r for r in self.reviews],
            "amenity_ids": self.amenity_ids
        }
