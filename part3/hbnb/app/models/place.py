from .BaseModel import BaseModel
from app import db


class Place(BaseModel, db.Model):
    """Place model for rental properties"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

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

        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id.strip()

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
        }
