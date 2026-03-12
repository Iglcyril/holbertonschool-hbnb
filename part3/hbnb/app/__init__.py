from flask import Flask
from flask_restx import Api

def create_app(config_class="config.DeveloppementConfig"): #ajout de la fonction config_class="config.DeveloppementConfig"
    app = Flask(__name__)
    app.config.from_object(config_class) #chargement de la configuration à partir de la classe spécifiée
    api = Api(
        app, 
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/' # modification du chemin de la documentation pour éviter les conflits avec les routes de l'API
        )

    from app.api.v1.users import api as users_ns            # j'ai déplacé car plus logique que ce soit a cette endroit du code, à voir 
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.places import api as places_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
