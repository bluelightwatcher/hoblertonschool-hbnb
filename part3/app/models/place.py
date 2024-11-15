from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.title_check(title)
        self.description = description
        self.price = self.price_check(price)
        self.latitude = self.latitude_check(latitude)
        self.longitude = self.longitude_check(longitude)
        self.owner = self.owner_check(owner)
        self.owner_id = owner.id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
    
    @staticmethod
    def price_check(price):
        if price <= 0:
            raise ValueError
        return price
    
    
    @staticmethod
    def title_check(title):
        if 0 <= len(title) <= 100:
            return title
        else:
            raise ValueError
    
    @staticmethod   
    def latitude_check(latitude):
        if not (-90 <= latitude <= 90):
            raise ValueError
        return latitude
        
    @staticmethod
    def longitude_check(longitude):
        if not (-180 <= longitude <= 180):
            raise ValueError
        return longitude
       
    def owner_check(self,owner):
        if not isinstance(owner, User):
            raise ValueError
        return owner
        
    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
             self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
             self.amenities.append(amenity)
