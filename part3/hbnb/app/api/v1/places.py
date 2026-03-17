from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            current_user = get_jwt_identity()
            data = request.get_json()
            data['owner_id'] = current_user
            new_place = facade.create_place(data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id
            }, 201
        except Exception as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id
        } for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"message": "Place not found"}, 404
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "created_at": place.created_at.isoformat(),
            "updated_at": place.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'You can only update your own place or be an admin')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            claims = get_jwt()
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            
            is_admin = claims.get('is_admin', False)
            user_id = claims.get('sub')
            
            if not is_admin and place.owner_id != user_id:
                return {'error': 'You can only update your own place or be an admin'}, 403
            
            data = request.get_json()
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {"error": "Place not found"}, 404
            return {
                "id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner_id,
                "created_at": updated_place.created_at.isoformat(),
                "updated_at": updated_place.updated_at.isoformat()
            }, 200
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.response(204, 'Place deleted successfully')
    @api.response(403, 'You can only delete your own place or be an admin')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        try:
            claims = get_jwt()
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            
            is_admin = claims.get('is_admin', False)
            user_id = claims.get('sub')
            
            if not is_admin and place.owner_id != user_id:
                return {'error': 'You can only delete your own place or be an admin'}, 403
            
            facade.delete_place(place_id)
            return '', 204
        except Exception as e:
            return {"error": "Internal server error"}, 500


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500
