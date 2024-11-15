from app.models.base_model import BaseModel
from app.extensions import bcrypt, db   
from sqlalchemy.orm import relationship
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    #places = relationship("Place", backref="user", lazy="dynamic")  # Relationship with Place
    #reviews = relationship("Review", backref="user", lazy="dynamic")  # Relationship with Review


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
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
