from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.text_check(text)
        self.rating = self.rating_check(rating)
        self.place = self.place_check(place)
        self.user = self.user_check(user)

    @staticmethod
    def text_check(text):
        if text < 1:
            raise ValueError("Text is too short")
        return text
    
    @staticmethod
    def rating_check(rating):
        if (0 <=  rating >= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
    

    @staticmethod
    def place_check(place.id):
        """check if place exists"""

    @staticmethod
    def user_check(user.id):
        """check if user exists"""
    