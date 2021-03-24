# imports the require libraries
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
        - email: will be the email of the user
        - pwd: will be the password of the user
        - image_name: the image name of the organizer
        - shows : relation between table Show
        - venues: relation between table Venue
        - artist: relation between table Artist
        - social: relation between table SocialOrganizer
        - names_organizer: will be the name of the organizer
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
        # takes the id of the organizer
        args[0]["organizer_id"] = self.id
        # create an instance of the class Show()
        show = Show()
        for key, value in args[0].items():
            # set each value in the dictionary
            setattr(show, key, value)
        try:
            # save the show object into a db
            show.save()
            return show
        except exc.IntegrityError as e:
            errorInfo = e.orig.args
            # This will give you error code
            print(errorInfo[0])
            # This will give you error message
            print(errorInfo[1])

    def create_venue(self, *args, **kwargs):
        """Create venue for Organizer"""
        # takes the id of the organizer
        args[0]["organizer_id"] = self.id
        # create an instance of the class Venue()
        venue = Venue()
        for key, value in args[0].items():
            # set each value in the dict
            setattr(venue, key, value)
        try:
            # save the venues object into a db
            venue.save()
            return venue
        except exc.IntegrityError as e:
            errorInfo = e.orig.args
            # This will give you error code
            print(errorInfo[0])
            # This will give you error message
            print(errorInfo[1])

    def create_artist(self, *args, **kwargs):
        """Create artits for Organizer"""
        # takes the id of the organizer
        args[0]["organizer_id"] = self.id
        # create an instance of the class Artist()
        artist = Artist()
        for key, value in args[0].items():
            setattr(artist, key, value)
        try:
            # save the artist into a db
            artist.save()
            return artist
        except exc.IntegrityError as e:
            print("artist")
            errorInfo = e.orig.args
            # This will give you error code
            print(errorInfo[0])
            # This will give you error message
            print(errorInfo[1])
