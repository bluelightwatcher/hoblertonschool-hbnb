from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import facade
from werkzeug.exceptions import BadRequest

api = Namespace('amenities', description='Amenity operations')
error = BadRequest('Invalid input data')
not_found_error = BadRequest('Amenity not found')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
amenity_response_model = api.model('Amenity_response', {
    'id': fields.String(required=True, description='id of the amenity'),
    'name': fields.String(required=True, description='name of the amenity')
})
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError:
            raise error
        return marshal(amenity, amenity_response_model)

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        return marshal(facade.get_all_amenities(), amenity_response_model), 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.expect('amenity_id')
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = (facade.get_amenity(amenity_id))
        except ValueError:
            raise not_found_error
        return marshal(amenity, amenity_response_model, 200)

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        amenity_data = api.payload
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError:
            raise not_found_error
        return {f"message": "Amenity updated successfully"}, 200