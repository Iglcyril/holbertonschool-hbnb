from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
 
import config
 
bcrypt = Bcrypt()  # Initialisation de Bcrypt pour le hachage des mots de passe
db = SQLAlchemy()  # Initialisation de SQLAlchemy pour la gestion de la base de données
jwt = JWTManager()  # Initialisation de JWT pour la gestion des tokens d'authentification
 
def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)  # Chargement de la configuration
    
    # Configure API with JWT authorization for Swagger UI
    api = Api(
        app, 
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** format'
            }
        },
        security='Bearer'
    )
 
    # Import and register API namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
 
    # Initialize Flask extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
 
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
