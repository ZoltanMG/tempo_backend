# imports the require libraries
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Artist(BaseModel, Base):
    """
    class Artist:
        - artist_name: type(string(60)) contains the name of the artist
        - organizer_id: type(string(60)) contains the id of the organizer
        - image_name: type(string(255)) contains the image of the artist
        - genre_artist: type(string(80)) contains the genre of the artist
        - social:  it is a relation between the table SocialArtist
    """
    __tablename__ = 'artists'
    artist_name = Column(String(60), nullable=False)
    organizer_id = Column(String(60), ForeignKey(
        'organizers.id'), nullable=False)
    image_name = Column(String(255), nullable=True)
    genre_artist = Column(String(80), nullable=False)
    social = relationship("SocialArtist", backref="artist",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    def shows(self):
        """
        takes all shows of an artist
        """
        from models.show import Show, ShowArtist
        # catch the artist id that is equeal to id in the table showArtist
        showArtists = models.storage.session.query(
            ShowArtist).filter_by(artist_id=self.id).all()
        listShows = []
        # create a list with an id show
        for sa in showArtists:
            listShows.append(sa.show_id)
        shows = []
        # and returns a list with the shows of this artist
        for show in listShows:
            shows.append(models.storage.session.query(
                Show).filter_by(id=show).first())
        return shows
