from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade
 
api = Namespace('amenities', description='Amenity operations')
 
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
 
 
@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin only')
    def post(self):
        """Register a new amenity - admin only"""
        claims = get_jwt()
 
        if not claims.get('is_admin'):
            return {'error': 'Forbidden: Admin access required'}, 403
 
        try:
            new_amenity = facade.create_amenity(api.payload)
            return new_amenity.to_dict(), 201
        except ValueError as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': 'Internal server error'}, 500
 
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities - public"""
        try:
            amenities = facade.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities], 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500
 
 
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID - public"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return amenity.to_dict(), 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500
 
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin only')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity - admin only"""
        claims = get_jwt()
 
        if not claims.get('is_admin'):
            return {'error': 'Forbidden: Admin access required'}, 403
 
        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return updated_amenity.to_dict(), 200
        except (ValueError, TypeError) as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': str(err)}, 500
 