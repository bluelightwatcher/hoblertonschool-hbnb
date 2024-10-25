from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place    
from app.models.review import Review  

class HBnBFacade:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
               
    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("user not foud")
            return 404

        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']

        self.user_repo.update(user.id, {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            })
        return user
    


    @classmethod
    def create_review(self, review_data):
        review_id = self.next_id
        review_data['review_id'] = review_id
        self.reviews[review_id] = review_data
        self.next_id += 1
        return review_data

    def get_review(self, review_id):
        return self.reviews.get(review_id, None)

    def get_all_reviews(self):
        return list(self.reviews.values())

    def get_reviews_by_place(self, place_id):
         return [review for review in self.reviews.values() if review['place_id'] == place_id]

    def update_review(self, review_id, review_data):
        if review_id in self.reviews:
            self.reviews[review_id].update(review_data)
            return self.reviews[review_id]
        return None

    def delete_review(self, review_id):
        return self.reviews.pop(review_id, None) is not None

    def create_place(self, place_data):
        """poping owner_id from api payload"""
        owner_id = place_data.get('owner_id', None)
        """geting the owner object from the repo"""
        owner = self.get_user(owner_id)
        if owner is None:
            raise ValueError(f"Owner ID : {owner_id} not found")
                
        """removing the reviews and amenities from the payload"""
        reviews = place_data.pop('reviews', [])
        amenities = place_data.pop('amenities', [])

        """creating the place and adding the owner object"""
        place = Place(**place_data)

        """adding back previously removed field"""
        place.reviews = reviews
        place.amenities = amenities

        """storing the place in repo"""
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        pass

facade =  HBnBFacade()