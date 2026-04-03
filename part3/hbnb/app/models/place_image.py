from app import db
from app.models.BaseModel import BaseModel


class PlaceImage(BaseModel):
    """PlaceImage model for storing multiple images per place"""

    __tablename__ = 'place_images'

    image_url = db.Column(db.String(500), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

    def __init__(self, image_url, place_id, is_primary=False):
        if not isinstance(image_url, str) or not image_url.strip():
            raise ValueError("image_url cannot be empty")
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("place_id cannot be empty")

        self.image_url = image_url.strip()
        self.place_id = place_id.strip()
        self.is_primary = is_primary

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "place_id": self.place_id,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
