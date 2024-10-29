from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import facade
from werkzeug.exceptions import BadRequest

api = Namespace('places', description='Place operations')
error = BadRequest('Invalid input data')
not_found_error = BadRequest('Place not found')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# Defines input validation for place creation request
place_creation_model = api.model('Place_creation', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})
# Defines the output requested following the place creation 
place_creation_response_model = api.model('Place_creation_response', {
    'id': fields.String(required=True, description='id of the place'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

# Defines the response mode for a get place request
place_get_response_model = api.model('Place_creation_response', {
    'id': fields.String(required=True, description='id of the place'),
    'title': fields.String(required=True, description='Title of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
})
# Defines the response model for a get place by if request
place_detail_response_model = api.model('Place_detail_get_response', {
    'id': fields.String(required=True, description='id of the place'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_creation_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try: 
            facade.create_place(place_data)
        except (ValueError):
            raise error
        return marshal(place_data, place_creation_response_model), 201  # Return the response with status code 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        return marshal(all_places, place_get_response_model)

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place is None:
            raise not_found_error
        return marshal(place, place_detail_response_model), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
        except ValueError:
            raise not_found_error
        return {'message': 'place successfully updated'}, 200