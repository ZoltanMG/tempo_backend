# imports the require libraries
import models
import datetime
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class ShowArtist(BaseModel, Base):
    """
    This class contains the items as follows:
        - artist_id: the id of the artist
        - show_id : the id of the show
        - artists : the relation between the table Artist
    """
    __tablename__ = 'shows_artists'
    artist_id = Column(String(60), ForeignKey(
        'artists.id'), nullable=True)
    show_id = Column(String(60), ForeignKey(
        'shows.id'), nullable=False)
    artists = relationship("Artist", backref="shows_artists")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)


class Show(BaseModel, Base):
    """
    This class contains the items as follows:
        - name_show: the id of the artist
        - description_show : the id of the show
        - status_show : the relation between the table Artist
        - price_ticket : the price of the tocket show
        - date: date of the show
        - hour: hour of the show
        - image_name: nam image of the show
        - venue_id: the id of the venue relation
        - organizer_di: the id of the organizer relation
        - show_artists: relation between ShowArtist
    """
    __tablename__ = 'shows'
    name_show = Column(String(60), nullable=True)
    description_show = Column(String(500), nullable=False)
    status_show = Column(String(60), nullable=False)
    price_ticket = Column(String(250), nullable=False)
    date = Column(DateTime, nullable=False)
    hour = Column(String(60), nullable=False)
    image_name = Column(String(255), nullable=True)
    venue_id = Column(String(60), ForeignKey("venues.id"), nullable=False)
    organizer_id = Column(String(60), ForeignKey(
        'organizers.id'), nullable=False)
    show_artists = relationship("ShowArtist", backref="show")

    def artists(self):
        """
        takes all the artists of a show
        """
        from models.artist import Artist
        # filter by show id
        showArtists = models.storage.session.query(
            ShowArtist).filter_by(show_id=self.id).all()
        listArtists = []
        for sa in showArtists:
            # push the id of the artist into a list
            listArtists.append(sa.artist_id)
        artistas = []
        for artista in listArtists:
            artistas.append(models.storage.session.query(
                Artist).filter_by(id=artista).first())
        return artistas

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
