from app.models.base_model import BaseModel
import re
from app.extensions import bcrypt, db   

class User(BaseModel):

    def __init__(self,first_name, last_name, email, password, is_admin=False):
        super().__init__()
        #from app import bcrypt
        self.first_name = self.first_name_check(first_name)
        self.last_name = self.last_name_check(last_name)
        self.is_admin = is_admin
        self.email = self.email_check(email)
        self.places = []
        self.reviews = []
        self.hash_password(password)

    @staticmethod
    def first_name_check(first_name):
        if  len(first_name) > 50:
            raise ValueError("name is too long")
        elif not isinstance (first_name, str):
            raise TypeError("Name must be a string")
        return first_name

    @staticmethod
    def last_name_check(last_name):
        if  len(last_name) > 50:
            raise ValueError("name is too long")
        elif not isinstance (last_name, str):
            raise TypeError("Name must be a string")
        return last_name

    @staticmethod
    def email_check(email):
        regex = r'^[a-zA-Z0-9.+-]+@[a-zA-Z]+\.[a-zA-Z0-9]{2,}+$'
        if not re.match(regex, email):
            raise ValueError
        return email 

    def add_place(self, place):
        self.places.append(place)

    def add_review(self, review):
        self.reviews.append(review)

    def hash_password(self, password):
        #from app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        #from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
