from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place  
from app.models.amenity import Amenity
from flask_restx import marshal
from flask import Flask, jsonify

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
        return place_data

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        pass

# Amenity method

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("amenity not foud")

        for key, value in amenity_data.items():
            if hasattr(amenity, key):  
                setattr(amenity, key, value)


        self.amenity_repo.update(amenity.id, amenity_data)
        return amenity
  

# Review method 

    @classmethod
    def create_review():
        pass

facade =  HBnBFacade()