from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user_id):
        super().__init__()
        self.text = self.text_check(text)
        self.rating = self.rating_check(rating)
        self.place = self.place_check(place)
        self.user = self.user_check(user_id)

    @staticmethod
    def text_check(text):
        if text < 1:
            raise ValueError("Text is too short")
        return text
    
    @staticmethod
    def rating_check(rating):
        if (0 <=  rating <= 5):
            return rating
        else:
            raise ValueError("Rating must be between 1 and 5")
        
    
    """ 
    @staticmethod
    def place_check(place):
    if not hasattr(place, 'id'):
        raise ValueError("Invalid place object")
    return place
    """ 
    """
    @staticmethod
    def user_check(user.id):
        check if user exists
        pass
    """