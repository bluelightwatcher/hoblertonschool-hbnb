from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place  
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls)
            cls._instance.user_repo = InMemoryRepository()
            cls._instance.place_repo = InMemoryRepository()
            cls._instance.review_repo = InMemoryRepository()
            cls._instance.amenity_repo = InMemoryRepository()
        return cls._instance

    """
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    

    def isadmin(self, user_id, owner_id):
            print(f"user_id {user_id} from the isadmin method itself")
            print(f"owner_id {owner_id} from the isadmin method itself")
            if owner_id == user_id:
                print("if true")
                return True
            else:
                print("if False")
                return False
    


    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return (user)

    
    def get_user(self, id): 
        return self.user_repo.get(id)
    

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
               
    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("user not foud")

        for key, value in user_data.items():
            if hasattr(user, key):  
                setattr(user, key, value)


        self.user_repo.update(user.id, user_data)
        return user
    



# Place method

    def create_place(self, place_data):
        """Create_place removes the owner_id from the paylod
        fetch the user object with the owner_id
        create the place
        stores the place
        adds the owner_id back for proper client response"""

        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        place_data['owner'] = owner
        place = Place(**place_data)
        self.place_repo.add(place)
        place_data['owner_id'] = owner_id
        place_data['id'] = place.id
        return place_data

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, user_id, place_data):
        place = self.get_place(place_id)
        print(f"Place with id {place_id} passed to update methode in the facade.")
        
        if not place:
            print(f"Place with id {place_id} not found from the update method.")
            raise ValueError
        
        owner_id = place.owner_id
        print(f"Owner_id {owner_id} retrieved from update_method")
        
        if self.isadmin(user_id, owner_id) is False:
            print(f"Place with id {place_id} not after isadmin in the update method.")
            raise ValueError

        for key, value in place_data.items():
            if hasattr(place, key):  
                setattr(place, key, value)


        self.place_repo.update(place.id, place_data)
        return place

# Amenity method

    def create_amenity(self, amenity_data):
        """pop unecessary data from payload
        create and store review in the repository
        attached review to the place instance
        """
        place_id = amenity_data.pop('place_id')
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        place = self.get_place(place_id)
        place.add_amenity(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError

        for key, value in amenity_data.items():
            if hasattr(amenity, key):  
                setattr(amenity, key, value)


        self.amenity_repo.update(amenity.id, amenity_data)
        return amenity
  

# Review method 

    def create_review(self, review_data):
        """ to create a review we first pop unecessecary data from the payload
        then create the review and store it
        adding the review to the place instance
        finally adding back necessary data for the client response
        """
        user_id = review_data.pop('user_id')
        user = self.get_user(user_id)
        review_data['user'] = user
        place_id = review_data.pop('place_id')
        place = self.get_place(place_id)
        review_data['place'] = place        
        review = Review(**review_data)
        self.review_repo.add(review)
        place.add_review(review)
        review.user_id = user_id
        review.place_id = place_id
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

facade =  HBnBFacade()