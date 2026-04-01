from app import db
from app.models.BaseModel import BaseModel
 
 
class Review(BaseModel):
    """Review model for place ratings and comments (SQLAlchemy mapped)"""
 
    __tablename__ = 'reviews'
 
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
 
    user = db.relationship('User', backref='reviews', lazy=True)
 
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )
 
    def __init__(self, text, rating, place_id, user_id):
        """Initialize a new Review instance
 
        Args:
            text: Review text content
            rating: Rating value (1-5)
            place_id: ID of the place being reviewed
            user_id: ID of the user who wrote the review
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text cannot be empty")
 
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
 
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place ID must be a non-empty string")
 
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string")
 
        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id.strip()
        self.user_id = user_id.strip()
 
    def to_dict(self):
        """Convert Review object to dictionary format"""
        # Include user name if relationship is loaded
        user_name = 'Anonymous'
        if self.user:
            user_name = f"{self.user.first_name} {self.user.last_name}"
 
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "user_name": user_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
 