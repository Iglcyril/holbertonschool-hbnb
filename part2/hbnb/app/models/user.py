from .BaseModel import BaseModel


class User(BaseModel):
    """User model for application users"""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a new User instance

        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            is_admin: Boolean indicating if user has admin privileges
        """
        super().__init__()

        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name must be a string and can't be empty")
        if len(first_name.strip()) > 50:
            raise ValueError("First name : 50 charaters max")

        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name must be a string and can't be empty")
        if len(last_name.strip()) > 50:
            raise ValueError("Last name : 50 characters max")

        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email can't be empty")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Email adress format not valid")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin

    def __str__(self):
        """String representation of the User object"""
        return f"[User] ({self.id}) {self.first_name} {self.last_name}"

    def to_dict(self):
        """Convert User object to dictionary format"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
