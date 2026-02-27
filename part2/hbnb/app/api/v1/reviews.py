from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True,
        description='Rating of the place (1-5)'
    ),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            new_review = facade.create_review(api.payload)
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

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            updated_review = facade.update_review(review_id, api.payload)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return updated_review.to_dict(), 200
        except ValueError as err:
            return {'error': str(err)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            result = facade.delete_review(review_id)
            if not result:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review successfully deleted'}, 200
        except Exception as err:
            return {'error': 'internal server error'}, 500
