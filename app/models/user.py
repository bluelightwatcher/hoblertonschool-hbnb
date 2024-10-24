from app.models.base_model import BaseModel
import re


class User(BaseModel):
        def __init__(self,first_name, last_name, email, is_admin=False):
                super().__init__()
                self.first_name = self.first_name_check(first_name)
                self.last_name = self.last_name_check(last_name)
                self.is_admin = is_admin 

                self.email = self.email_check(email)

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
                    raise ValueError("Email must follow standard email format.")
                return email 
       
        
        @classmethod
        def add_place():
               pass

        @classmethod
        def add_review():
               pass       