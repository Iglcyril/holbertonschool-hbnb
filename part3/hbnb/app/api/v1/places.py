from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'image_url': fields.String(description='URL of the place image')
})
 
 
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    def post(self):
        """Register a new place - requires authentication"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
 
        try:
            data = request.get_json()
 
            # Regular users can only create places for themselves
            if not claims.get('is_admin') and data.get('owner_id') != current_user_id:
                return {'error': 'Unauthorized: You can only create places for yourself'}, 403
 
            new_place = facade.create_place(data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id,
                "amenities": [amenity.id for amenity in new_place.amenities]
            }, 201
        except Exception as e:
            return {"message": str(e)}, 400
 
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places - public"""
        places = facade.get_all_places()
        return [{
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": [amenity.id for amenity in place.amenities],
            "image_url": place.image_url,
        } for place in places], 200
 
 
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID - public"""
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
            "image_url": place.image_url,
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email,
                "bio": place.owner.bio,
                "profile_picture_url": place.owner.profile_picture_url
            },
            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name
                } for amenity in place.amenities
            ],
            "reviews": [review.to_dict() for review in place.reviews],
            "images": [img.to_dict() for img in place.images]
        }, 200
 
    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place - owner or admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
 
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
 
        # Only owner or admin can update
        if not claims.get('is_admin') and place.owner_id != current_user_id:
            return {'error': 'Forbidden: You can only update your own places'}, 403
 
        try:
            data = request.get_json()
            updated_place = facade.update_place(place_id, data)
            return {
                "id": updated_place.id,
                "title": updated_place.title,
                "description": updated_place.description,
                "price": updated_place.price,
                "latitude": updated_place.latitude,
                "longitude": updated_place.longitude,
                "owner_id": updated_place.owner_id,
                "amenities": [amenity.id for amenity in updated_place.amenities],
                "created_at": updated_place.created_at.isoformat(),
                "updated_at": updated_place.updated_at.isoformat()
            }, 200
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Internal server error"}, 500

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place - owner or admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not claims.get('is_admin') and place.owner_id != current_user_id:
            return {'error': 'Forbidden: You can only delete your own places'}, 403

        facade.place_repo.delete(place_id)
        return {"message": "Place deleted successfully"}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place - public"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
 
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500