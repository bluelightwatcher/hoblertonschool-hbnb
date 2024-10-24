from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the user model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='title of the place'),
    'price': fields.Float(required=True, description='the price is a user input'),
    'description': fields.String(required=False, description='description of the place'),
    'latitude': fields.Float(required=True, description='latitude coordinate'),
    'longitude': fields.Float(required=True, description='longitude coordinate'),
    'owner': fields.String(required=True, description='define is user is admin')
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
    })

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'coordinate already registered')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        owner_id = place_data.get("owner")
        user_id = facade.get_user(owner_id)
        if user_id is None:
            return{'error': 'Owner not found'}, 400
        
        place_data['owner'] = user_id

        new_place = facade.create_place(**place_data)
        
        response_data = {
            'id': new_place.id,  # Assuming `new_place` has an `id` attribute
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': new_place.owner
            }

        return response_data, 201  # Return the response with status code 201