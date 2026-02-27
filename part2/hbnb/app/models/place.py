from .BaseModel import BaseModel


class Amenity(BaseModel):
    """Amenity model for place features"""

    def __init__(self, name):
        """Initialize a new Amenity instance
        
        Args:
            name: Name of the amenity
        """
        super().__init__()

        if not isinstance(name, str):
            raise TypeError("name must be a string")

        if len(name) > 50:
            raise ValueError("name must be 50 characters or less")

        if not name.strip():
            raise ValueError("name cannot be empty")

        self.name = name.strip()

    def __str__(self):
        """String representation of the Amenity object"""
        return f"Amenity(id='{self.id}', name='{self.name}')"

    def to_dict(self):
        """Convert Amenity object to dictionary format"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
