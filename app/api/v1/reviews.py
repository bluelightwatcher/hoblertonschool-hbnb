from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
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
            # Extract data from the request
            review_data = api.payload
            # Call the facade service to create a review
            created_review = facade.create_review(review_data)
            return created_review, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            # Call the facade service to get all reviews
            reviews = facade.get_all_reviews()
            return reviews, 200
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            # Call the facade service to get a review by ID
            review = facade.get_review(review_id)
            if review:
                return review, 200
            else:
                api.abort(404, 'Review not found')
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            # Extract the new review data from the request
            review_data = api.payload
            # Call the facade service to update the review
            updated_review = facade.update_review(review_id, review_data)
            if updated_review:
                return updated_review, 200
            else:
                api.abort(404, 'Review not found')
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            # Call the facade service to delete the review
            success = facade.delete_review(review_id)
            if success:
                return {'message': 'Review deleted successfully'}, 200
            else:
                api.abort(404, 'Review not found')
        except Exception as e:
            api.abort(500, str(e))

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            # Call the facade service to get reviews for a specific place
            reviews = facade.get_reviews_by_place(place_id)
            if reviews:
                return reviews, 200
            else:
                api.abort(404, 'Place not found or no reviews for this place')
        except Exception as e:
            api.abort(500, str(e))