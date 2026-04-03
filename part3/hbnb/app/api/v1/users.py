from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
 
api = Namespace('users', description='User related operations')
 
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})
 
 
@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin only')
    def post(self):
        """Register a new user - admin only"""
        claims = get_jwt()
 
        if not claims.get('is_admin'):
            return {'error': 'Forbidden: Admin access required'}, 403
 
        try:
            user_data = api.payload
 
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
 
            new_user = facade.create_user({
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': user_data['password']
            })
 
            return {
                'message': 'User successfully created',
                'id': new_user.id,
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500
 
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get a list of all users - public"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200
 
 
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID - public"""
        user = facade.get_user(user_id)
 
        if not user:
            return {'error': 'User not found'}, 404
 
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'bio': user.bio,
            'profile_picture_url': user.profile_picture_url
        }, 200
 
    @jwt_required()
    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Email already registered')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details - owner or admin only"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
 
        # Only owner or admin can update
        if not claims.get('is_admin') and current_user_id != user_id:
            return {'error': 'Forbidden: You can only update your own account'}, 403
 
        try:
            user_data = api.payload
 
            # Validate first_name
            if 'first_name' in user_data:
                first_name = user_data['first_name']
                if not isinstance(first_name, str) or not first_name.strip():
                    return {'error': 'First name must be a string and can\'t be empty'}, 400
                if len(first_name.strip()) > 50:
                    return {'error': 'First name: 50 characters max'}, 400
 
            # Validate last_name
            if 'last_name' in user_data:
                last_name = user_data['last_name']
                if not isinstance(last_name, str) or not last_name.strip():
                    return {'error': 'Last name must be a string and can\'t be empty'}, 400
                if len(last_name.strip()) > 50:
                    return {'error': 'Last name: 50 characters max'}, 400
 
            # Validate email
            if 'email' in user_data:
                email = user_data['email']
                if not isinstance(email, str) or not email.strip():
                    return {'error': 'Email can\'t be empty'}, 400
                if "@" not in email or "." not in email.split("@")[-1]:
                    return {'error': 'Email address format not valid'}, 400
 
                existing_user = facade.get_user_by_email(email.strip().lower())
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already registered'}, 400
 
            # Only admin can change is_admin
            if 'is_admin' in user_data and not claims.get('is_admin'):
                return {'error': 'Forbidden: Only admin can change is_admin'}, 403
 
            updated_user = facade.update_user(user_id, user_data)
 
            if not updated_user:
                return {'error': 'User not found'}, 404
 
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'bio': updated_user.bio,
                'profile_picture_url': updated_user.profile_picture_url
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500
 
    @jwt_required()
    @api.response(200, 'User deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - Admin only')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user - admin only"""
        claims = get_jwt()
 
        if not claims.get('is_admin'):
            return {'error': 'Forbidden: Admin access required'}, 403
 
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
 
        facade.user_repo.delete(user_id)
        return {'message': 'User successfully deleted'}, 200
 