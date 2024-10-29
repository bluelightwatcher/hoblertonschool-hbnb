from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import facade
from werkzeug.exceptions import BadRequest


api = Namespace('users', description='User operations')
error = BadRequest('Invalid input data')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user',)
})
user_response_model = api.model('User_response', {
    'id' : fields.String(required=True, description='Id of the user inherited from base model'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new user"""
        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            raise error
        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError):
            raise error
        return marshal(new_user, user_response_model), 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.marshal_with(user_response_model, code=200)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            raise error 
        else:
            return marshal(user, user_response_model), 201
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response_model, code=200)
    def put(self, user_id):
        """Register a new user"""
        user_data = api.payload

        user = facade.update_user(user_id, user_data)
        if not user:
            raise error
        else:
            return user