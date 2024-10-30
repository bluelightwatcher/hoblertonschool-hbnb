from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define the review model response
review_response_model = api.model('Review_response_model', {
    'id': fields.String(required=True, description='Id of the review object'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
# Define the review list response
review_list_response_model = api.model('Review_list_response_model', {
    'id': fields.String(required=True, description='Id of the review object'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

# Define the review update payload
review_update_model = api.model('Review_update_model', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        review = facade.create_review(review_data)
        return marshal(review, review_response_model), 201
        

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        review_list = facade.review_repo.get_all()
        return marshal(review_list, review_list_response_model)

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        return marshal(review, review_response_model), 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        facade.update_review(review_id, review_data)
        return ("message : review updated sucessfully"), 200
    
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        facade.delete_review(review_id)
        return ("message : review deleted succesfully"), 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        review_by_place = facade.get_reviews_by_place(place_id)
        return marshal(review_by_place, review_list_response_model), 200