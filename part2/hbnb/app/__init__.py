#task 0 
#3.Set Up the Flask Application with Placeholders
#Inside the app/ directory, create the Flask application instance within the __init__.py file:
#line 5 - 15
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    return app