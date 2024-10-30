from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.text_check(text)
        self.rating = self.rating_check(rating)
        self.place = self.place_check(place)
        self.user = self.user_check(user)

    @staticmethod
    def text_check(text):
        if len(text) < 1:
            raise ValueError
        return text
    
    @staticmethod
    def rating_check(rating):
        if (0 <=  rating <= 5):
            return rating
        else:
            raise ValueError
        
    
    
    @staticmethod
    def place_check(place):
        if not isinstance(place, Place):
            raise ValueError
        return place
     
    
    @staticmethod
    def user_check(user):
        if not isinstance(user, User):
            raise ValueError
        return user
    