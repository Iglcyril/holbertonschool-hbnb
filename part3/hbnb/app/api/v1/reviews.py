from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            current_user = get_jwt_identity()
            data = api.payload
            place_id = data.get('place_id')

            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if user is the owner of the place
            if place.owner_id == current_user:
                return {'error': 'You cannot review your own place'}, 400

            # Check if user has already reviewed this place
            all_reviews = facade.get_all_reviews()
            for review in all_reviews:
                if review.user_id == current_user and review.place_id == place_id:
                    return {'error': 'You have already reviewed this place'}, 400

            # Set user_id to current_user
            data['user_id'] = current_user
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [review.to_dict() for review in reviews], 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return review.to_dict(), 200
        except Exception as err:
            return {'error': 'Internal server error'}, 500

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'You can only update your own review or be an admin')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            claims = get_jwt()
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            is_admin = claims.get('is_admin', False)
            user_id = claims.get('sub')

            if not is_admin and review.user_id != user_id:
                return {'error': 'You can only update your own review or be an admin'}, 403

            updated_review = facade.update_review(review_id, api.payload)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return updated_review.to_dict(), 200
        except (ValueError, TypeError) as err:
            return {'error': str(err)}, 400
        except Exception as err:
            return {'error': 'Internal server error'}, 500

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(403, 'You can only delete your own review or be an admin')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            claims = get_jwt()
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            is_admin = claims.get('is_admin', False)
            user_id = claims.get('sub')

            if not is_admin and review.user_id != user_id:
                return {'error': 'You can only delete your own review or be an admin'}, 403

            result = facade.delete_review(review_id)
            if not result:
                return {'error': 'Review not found'}, 404
            return '', 204
        except Exception as err:
            return {'error': 'Internal server error'}, 500
