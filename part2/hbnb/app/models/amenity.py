from .BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not isinstance(name, str):
            raise TypeError("name must be a string")
        
        if len(name) > 50:
            raise ValueError("name must be 50 characters or less")

        if not name.strip():
            raise ValueError("name cannot be empty")
        
        self.name = name.strip()

    def __str__(self):
        return f"Amenity(id='{self.id}', name='{self.name}')"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
