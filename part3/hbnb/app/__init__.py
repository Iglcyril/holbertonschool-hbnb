from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import config

#import config --> pas sur qu'il faille cet import car j'ai une erreur  is not accessed à voir

bcrypt = Bcrypt() #initialisation de Bcrypt pour le hachage des mots de passe
db = SQLAlchemy() #initialisation de SQLAlchemy pour la gestion de la base de données
jwt = JWTManager() #initialisation de JWT pour la gestion des tokens d'authentification

def create_app(config_class="config.DevelopmentConfig"): #ajout de la fonction config_class="config.DeveloppementConfig"
    app = Flask(__name__)
    app.config.from_object(config_class) #chargement de la configuration à partir de la classe spécifiée
    api = Api(
        app, 
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='' # modification du chemin de la documentation pour éviter les conflits avec les routes de l'API
        )

    from app.api.v1.users import api as users_ns            # j'ai déplacé car plus logique que ce soit a cette endroit du code, à voir 
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    bcrypt.init_app(app) #initialisation de Bcrypt avec l'application Flask
    db.init_app(app) #initialisation de SQLAlchemy avec l'application Flask
    jwt.init_app(app) #initialisation de JWT avec l'application Flask

    with app.app_context():
        db.create_all() #création des tables dans la base de données
    return app
