from app import db
from app import bcrypt
from app.models.BaseModel import BaseModel


class User(BaseModel):
    """User model for application users (SQLAlchemy mapped)"""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.String(500), nullable=True)
    profile_picture_url = db.Column(db.String(500), nullable=True)
    

    def __init__(self, first_name, last_name, email, is_admin=False, password=None, bio=None, profile_picture_url=None):
        """Initialize a new User instance

        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            is_admin: Boolean indicating if user has admin privileges
            password: User's password (will be hashed)
        """
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name must be a string and can't be empty")
        if len(first_name.strip()) > 50:
            raise ValueError("First name : 50 characters max")

        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("Last name must be a string and can't be empty")
        if len(last_name.strip()) > 50:
            raise ValueError("Last name : 50 characters max")

        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email can't be empty")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Email address format not valid")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean value")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.is_admin = is_admin
        self.bio = bio
        self.profile_picture_url = profile_picture_url

        self.password = None
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hash a password using bcrypt"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a password against the stored hash"""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

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
            "bio": self.bio,
            "profile_picture_url": self.profile_picture_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
