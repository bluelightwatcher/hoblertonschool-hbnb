from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import facade
from werkzeug.exceptions import BadRequest
from app.extensions import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')
error = BadRequest('Invalid input data')

# Define the user model for input validation and documentation
user_creation_model = api.model('User_creation', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(require=True, description='Password of the user')
})

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_update_model = api.model('User_update_model', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})
# Define the user model response
user_response_model = api.model('User_response', {
    'id' : fields.String(required=True, description='Id of the user inherited from base model'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_creation_model, validate=True)
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
    def get(self, user_id):
        #from app.extensions import jwt_required, get_jwt_identity
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            raise error 
        else:
            return marshal(user, user_response_model), 200
    
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Only user can modify their information')
    @api.marshal_with(user_response_model, code=200)
    @jwt_required()
    def put(self, user_id):
        """Update User's details"""
        current_user = get_jwt_identity()
        if current_user == None:
            return(f"please login")
        requestor_id = current_user["id"]
        if requestor_id != user_id:
            return { "message": "Only user can modify their information"}, 403

        user_data = api.payload
        user = facade.update_user(user_id, user_data)
        if not user:
            raise error
        else:
            return user
