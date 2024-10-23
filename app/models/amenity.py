class Amenity(BaseModel):
    super().__init__()
        self.name = self.name_check(name)

    @staticmethod
    def name_check(name):
        if < 2 len(name) > 50:
            return name
        else:
            raise ValueError("name must be between 2 and 50 characters")