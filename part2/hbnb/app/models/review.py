from .BaseModel import BaseModel

class Review(BaseModel):
    
    def __init__(self, text, rating, place_id, user_id):
       
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Please write a review")
    
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating beetween 0 and 5.")

        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place must be a string.")
    
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User must be an string")

        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id.strip()
        self.user_id = user_id.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
