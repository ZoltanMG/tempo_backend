import models
import datetime
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


"""Representation of Show """


class ShowArtist(BaseModel, Base):

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
    """Representation of Show """
    __tablename__ = 'shows'
    # artist_id = Column(String(300), ForeignKey(
    #     'artists.id'), nullable=False)
    name_show = Column(String(60), nullable=True)
    description_show = Column(String(500), nullable=False)
    status_show = Column(String(60), nullable=False)
    price_ticket = Column(String(250), nullable=False)
    # verificar a cambiar por tipo de dato DATETIME
    date = Column(DateTime, nullable=False)
    hour = Column(String(60), nullable=False)
    image_name = Column(String(255), nullable=True)
    venue_id = Column(String(60), ForeignKey("venues.id"), nullable=False)
    organizer_id = Column(String(60), ForeignKey(
        'organizers.id'), nullable=False)
    show_artists = relationship("ShowArtist", backref="show")
    # (id=show.venue_id)

    def artists(self):
        """
        TRAER TODOS LOS ARTISTAS DE UN SHOW
        """
        from models.artist import Artist
        showArtists = models.storage.session.query(
            ShowArtist).filter_by(show_id=self.id).all()
        listArtists = []
        for sa in showArtists:
            listArtists.append(sa.artist_id)
        artistas = []
        for artista in listArtists:
            artistas.append(models.storage.session.query(
                Artist).filter_by(id=artista).first())
        return artistas

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
