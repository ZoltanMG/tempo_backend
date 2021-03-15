import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """
    Class City: create a city
        - city_name : type String
        - country_name : type String
        - id: inherits from basemodel
        - created_at : inherits from basemodel
        - updated_at : inherits from basemodel
    """
    __tablename__ = 'cities'
    city_name = Column(String(60), nullable=False)
    country_name = Column(String(60), nullable=False)
    state = Column(String(60), nullable=False)
    venues = relationship("Venue", backref="city",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
