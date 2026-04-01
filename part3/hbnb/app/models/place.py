from app import db
from app.models.BaseModel import BaseModel


# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """Place model for rental properties (SQLAlchemy mapped)"""
    
    __tablename__ = 'places'
    
    # SQLAlchemy columns
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    
    # Relationships
    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id, description='', image_url=None):
        """Initialize a new Place instance
        
        Args:
            title: Title of the place
            price: Price per night
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            owner_id: ID of the place owner
            description: Optional description of the place
        """
        # Validations
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

        if description and not isinstance(description, str):
            raise ValueError("Description must be a string")
        if description and len(description.strip()) > 500:
            raise ValueError("Description must not exceed 500 characters")

        # Set attributes
        self.title = title.strip()
        self.description = description.strip() if description else ""
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id.strip()
        self.image_url = image_url

    def add_amenity(self, amenity):
        """Add an amenity to the place
        
        Args:
            amenity: Amenity object to add
        """
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place
        
        Args:
            amenity: Amenity object to remove
        """
        if amenity in self.amenities:
            self.amenities.remove(amenity)

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
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
