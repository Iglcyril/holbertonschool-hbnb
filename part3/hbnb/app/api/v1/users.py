from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt, jwt_required
from app.services import facade

api = Namespace('users', description='User related operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email (admin only)'),
    'password': fields.String(required=False, description='Password (admin only)'),
    'is_admin': fields.Boolean(required=False, description='Admin flag')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user (admin only)"""
        try:
            claims = get_jwt()
            if not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403

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
        """Get a list of all users"""
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
        """Get user details by ID"""
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'You can only update your own profile or be an admin')
    @api.response(404, 'User not found')
    @api.response(400, 'You cannot modify email or password')
    def put(self, user_id):
        """Update user details"""
        try:
            claims = get_jwt()
            user_identity = claims.get('sub')
            is_admin = claims.get('is_admin', False)

            if not is_admin and user_identity != user_id:
                return {'error': 'You can only update your own profile or be an admin'}, 403

            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            user_data = api.payload
            # Prevent modification of email and password for non-admin users
            if not is_admin and ('email' in user_data or 'password' in user_data):
                return {'error': 'You cannot modify email or password'}, 400
            # Validate email uniqueness when admin modifies email
            if 'email' in user_data and is_admin:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400
            updated_user = facade.update_user(user_id, user_data)

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @jwt_required()
    @api.response(204, 'User deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user (admin only)"""
        try:
            claims = get_jwt()
            if not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403

            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            facade.delete_user(user_id)
            return '', 204
        except Exception as e:
            return {'error': 'Internal server error'}, 500
