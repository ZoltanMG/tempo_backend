import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class SocialArtist(BaseModel, Base):
    """
    class Social
    """
    __tablename__ = 'social_artist'
    artist_id = Column(String(60), ForeignKey("artists.id"), nullable=True)
    link = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
