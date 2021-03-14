from sqlalchemy import Column, Integer, String, Text, DATETIME
from models.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing":True}
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))
    height = Column(Integer)
    target_weight = Column(String(128))

    def __init__ (self, user_name=None, hashed_password=None, height=None, target_weight=None):
        self.user_name = user_name
        self.hashed_password = hashed_password
        self.height = height
        self.target_weight = target_weight



    def __repr__(self):
        return "User<{}, {}, {}, {}>" .format(self.user_name, self.hashed_password, self.height, self.target_weight)

class Weight (Base):
    __tablename__ = "weight"
    __table_args__ = {"extend_existing":True}
    user_name = Column(String(128), primary_key=True)
    date = Column(DATETIME)
    weight = Column(Integer)
    bmi = Column(Integer)
    difference = Column(Integer)

    def __init__ (self, user_name=None, date=None, weight=None, bmi=None, difference=None):
        self.user_name = user_name
        self.date = date
        self.weight = weight
        self.bmi = bmi
        self.difference = difference


    def __repr__(self):
        return "Weight<{}, {}, {}, {}>".format(self.user_name, self.date, self.time, self.weight, self.difference)
        

