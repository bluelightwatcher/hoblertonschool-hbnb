from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Define the user model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='title of the place'),
    'description': fields.String(required=False, description='description of the place'),
    'latitude': fields.Float(required=True, description='latitude coordinate'),
    'longitude': fields.Float(required=True, description='longitude coordinate'),
    'owner': fields.Boolean(required=True, description='define is user is admin')
})

facade = HBnBFacade()