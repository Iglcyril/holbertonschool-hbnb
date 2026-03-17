from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, jwt_required
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
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity (admin only)"""
        try:
            claims = get_jwt()
            if not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403

            new_amenity = facade.create_amenity(api.payload)
            return new_amenity.to_dict(), 201
        except ValueError as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
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
        """Get amenity details by ID"""

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
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information (admin only)"""
        try:
            claims = get_jwt()
            if not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403

            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return updated_amenity.to_dict(), 200
        except (ValueError, TypeError) as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': str(err)}, 500

    @jwt_required()
    @api.response(204, 'Amenity deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        try:
            claims = get_jwt()
            if not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403

            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            
            facade.delete_amenity(amenity_id)
            return '', 204
        except Exception as err:
            return {'error': 'Internal server error'}, 500
