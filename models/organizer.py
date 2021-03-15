import models
from models.base_model import BaseModel, Base
from models.venue import Venue
from models.artist import Artist
from models.show import Show
from os import getenv
import sqlalchemy
from sqlalchemy import exc
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_login import UserMixin


class Organizer(UserMixin, BaseModel, Base):
    """
    class Organizer:
        - username: username login

    """
    __tablename__ = 'organizers'
    email = Column(String(60), nullable=False)
    pwd = Column(String(250), nullable=False)
    image_name = Column(String(255), nullable=True)
    shows = relationship("Show", backref="organizer",
                         cascade="all, delete, delete-orphan")
    venues = relationship("Venue", backref="organizer",
                          cascade="all, delete, delete-orphan")
    artists = relationship("Artist", backref="organizer",
                           cascade="all, delete, delete-orphan")
    # social = Column(String(1000), nullable=True)
    names_organizer = Column(String(80), nullable=False)
    social = relationship("SocialOrganizer", backref="organizer",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    def create_show(self, *args, **kwargs):
        """Create show for organizer"""
        args[0]["organizer_id"] = self.id
        show = Show()
        for key, value in args[0].items():
            setattr(show, key, value)
        try:
            show.save()
            return show
        except exc.IntegrityError as e:
            print("show")
            errorInfo = e.orig.args
            print(errorInfo[0])  # This will give you error code
            print(errorInfo[1])  # This will give you error message

    def create_venue(self, *args, **kwargs):
        """Create venue for Organizer"""
        args[0]["organizer_id"] = self.id
        venue = Venue()
        for key, value in args[0].items():
            setattr(venue, key, value)
        try:
            venue.save()
            return venue
        except exc.IntegrityError as e:
            print("venue")
            errorInfo = e.orig.args
            print(errorInfo[0])  # This will give you error code
            print(errorInfo[1])  # This will give you error message

    def create_artist(self, *args, **kwargs):
        """Create artits for Organizer"""
        args[0]["organizer_id"] = self.id
        artist = Artist()
        for key, value in args[0].items():
            setattr(artist, key, value)
        try:
            artist.save()
            return artist
        except exc.IntegrityError as e:
            print("artist")
            errorInfo = e.orig.args
            print(errorInfo[0])  # This will give you error code
            print(errorInfo[1])  # This will give you error message
