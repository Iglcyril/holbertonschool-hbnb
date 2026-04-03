from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('place_images', description='Place images operations')

image_model = api.model('PlaceImage', {
    'image_url': fields.String(required=True, description='URL of the image'),
    'is_primary': fields.Boolean(description='Is this the primary image', default=False)
})


@api.route('/<place_id>/images')
class PlaceImageList(Resource):
    @api.response(200, 'List of images retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all images for a place - public"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [img.to_dict() for img in place.images], 200

    @jwt_required()
    @api.expect(image_model)
    @api.response(201, 'Image added successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def post(self, place_id):
        """Add an image to a place - owner or admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not claims.get('is_admin') and place.owner_id != current_user_id:
            return {'error': 'Forbidden: You can only add images to your own places'}, 403

        try:
            new_image = facade.create_place_image(place_id, api.payload)
            return new_image.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500


@api.route('/<place_id>/images/<image_id>')
class PlaceImageResource(Resource):
    @jwt_required()
    @api.response(200, 'Image deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Image not found')
    def delete(self, place_id, image_id):
        """Delete an image - owner or admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not claims.get('is_admin') and place.owner_id != current_user_id:
            return {'error': 'Forbidden'}, 403

        result = facade.delete_place_image(image_id)
        if not result:
            return {'error': 'Image not found'}, 404
        return {'message': 'Image deleted successfully'}, 200
