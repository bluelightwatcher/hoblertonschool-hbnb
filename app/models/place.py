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
        # self.owner_id = self.owner_check(owner_id)
        self.owner = self.owner_check(owner)
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
    
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
            else:
                result[key] = value.to_dict() if hasattr(value, 'to_dict') else value
        return result

    @staticmethod
    def price_check(price):
        if price < 0:
            raise ValueError("price must be positive")
        return price
    
    
    @staticmethod
    def title_check(title):
        if 0 <= len(title) <= 100:
            return title
        else:
            raise ValueError("Title is too long")
    
    @staticmethod   
    def latitude_check(latitude):
        if not (-90 <= latitude <= 90):
            raise ValueError("latitude not correct")
        return latitude
        
    @staticmethod
    def longitude_check(longitude):
        if not (-180 <= longitude <= 180):
            raise ValueError("longitude not correct")
        return longitude
       
    @staticmethod
    def owner_check(owner):
        if not isinstance(owner, User):
            raise ValueError(f"Owner {owner} must be a valid User instance")
        return owner
        
    @classmethod
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    @classmethod
    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)