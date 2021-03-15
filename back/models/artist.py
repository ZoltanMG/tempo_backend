import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Artist(BaseModel, Base):
    """
    class Organizer:
        - username: username login
    """
    __tablename__ = 'artists'
    artist_name = Column(String(60), nullable=False)  # , unique=True)
    organizer_id = Column(String(60), ForeignKey(
        'organizers.id'), nullable=False)
    image_name = Column(String(255), nullable=True)
    # social = Column(String(1000), nullable=True)
    genre_artist = Column(String(80), nullable=False)
    # email = Column(String(60), nullable=False)  # , unique=True)
    # shows = relationship("Show", backref="artist")
#    show_artists = relationship("Show", backref="artist") #####
    social = relationship("SocialArtist", backref="artist",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)


    def shows(self):
        """
        TRAER TODOS LOS SHOWS DE UN ARTISTA
        """
        from models.show import Show, ShowArtist
        showArtists = models.storage.session.query(
            ShowArtist).filter_by(artist_id=self.id).all()
        # listArtists = models.storage.session.query(
        #     Artist).filter_by(id=ShowArtist.artist_id).all()
        # # listArtistsId[showArtist.artist_id] = models.storage.session.query(
        # Artist).filter_by(id=showArtist.id).first()
        listShows = []
        for sa in showArtists:
            listShows.append(sa.show_id)
        shows = []
        for show in listShows:
            shows.append(models.storage.session.query(
                Show).filter_by(id=show).first())
        return shows
