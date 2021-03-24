# imports the require libraries
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship


class Venue(BaseModel, Base):
    """
    Class Venue: create a venue
        - city_id : type Forignkey wih the id of City
        - address : type String address of the place
        - id: inherits from basemodel
        - created_at : inherits from basemodel
        - updated_at : inherits from basemodel
        - phone: type String p'hone of the bar
        - social: the links of fb, instagram (bar, restaurant, etc)
        - capacity: the number max of people by bar
        - latitude: the latitude of the bar
        - longitude: the longitude of the bar
        - description: description of the bar
    """
    __tablename__ = 'venues'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    organizer_id = Column(String(60), ForeignKey(
        'organizers.id'), nullable=False)
    venue_name = Column(String(60), nullable=False)
    image_name = Column(String(255), nullable=True)
    address = Column(String(60), nullable=False)
    description = Column(String(250), nullable=True)
    shows = relationship("Show", backref="venue",
                         cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
