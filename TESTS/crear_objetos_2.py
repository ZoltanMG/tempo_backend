#!/usr/bin/python3
"""
SCRIPT QUE INCIALIZA CON FAKE DATA NUESTRA DB DE TEMPO
"""
import datetime
from models import storage
from models.city import City
from models.venue import Venue
from models.show import Show, ShowArtist
from models.artist import Artist
from models.social_organizer import SocialOrganizer
from models.social_artist import SocialArtist
from models.organizer import Organizer
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint

bogota = storage.session.query(City).filter_by(city_name="Bogotá").first()
print(bogota)
medellin = storage.session.query(City).filter_by(city_name="Medellín").first()


# Organizador
organizer =  storage.session.query(Organizer).first()


# Lugares
venue = {
    "city_id": bogota.id,
    "venue_name": "LOS OCARROS",
    "address": "Calle del cartucho",
    "phone": "23555",
    "capacity": "150",
    "latitude": "7.89",
    "longitude": "0.98",
    "description": "LOS OCARROS ES UN BAR QUE TE OFRECE MULTIPLES SERVICIOS ESTAMOS UBICADOS A DOS CUADRAS DEL PARQUE DE LOS NOVIOS :)"
}
venue_objeto = organizer.create_venue(venue)

venue2 = {
    "city_id": bogota.id,
    "venue_name": "LOS TINTEROS",
    "address": "Comuna 13",
    "phone": "376737326",
    "capacity": "200",
    "latitude": "8.90",
    "longitude": "0.100",
    "description": "LOS TINTEROS ES UN BAR QUE TE OFRECE MULTIPLES SERVICIOS ESTAMOS UBICADOS A DOS CUADRAS DEL PARQUE DE LAS FLORES :)"
}
venue_objeto2 = organizer.create_venue(venue2)

# Artistas
artista = {
    "artist_name": "tigres del norte",
    "genre_artist": "Norteña"
}
artista_objeto = organizer.create_artist(artista)

artista2 = {
    "artist_name": "tigres del norte",
    "genre_artist": "Norteña"
}
artista_objeto2 = organizer.create_artist(artista2)

artista3 = {
    "artist_name": "Olivia Rodrigo",
    "genre_artist": "Rock"
}
artista_objeto3 = organizer.create_artist(artista3)


# Redes Sociales Artista
social = SocialArtist(
    artist_id=artista_objeto.id,
    link="facebook.com/los-tigres-del-norte",
    description="Facebook"
)
social.save()

social2 = SocialArtist(
    artist_id=artista_objeto2.id,
    link="facebook.com/olivia",
    description="Facebook"
)
social2.save()

social3 = SocialArtist(
    artist_id=artista_objeto3.id,
    link="facebook.com/olivia",
    description="Facebook"
)
social3.save()


# Shows!
date_str = "2021-04-12"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date = datetime.datetime(year, month, day, 0, 0, 0)

show = {
    "name_show": "script 2 - show3 2021-04-12 en un mes Norteña bogotá",
    "status_show": "en curso",
    "price_ticket": "$250.000",
    "date": date,
    "hour": "8:00 pm",
    "venue_id": venue_objeto.id,
}
show_objeto = organizer.create_show(show)

date_str2 = "2021-03-08"
year = int(date_str2[0:4])
month = int(date_str2[5:7])
day = int(date_str2[8:10])
date2 = datetime.datetime(year, month, day, 0, 0, 0)
show2 = {
    "name_show": "script 2 - show3 2021-03-08 hoy Norteña Medellín",
    "status_show": "cancelado",
    "price_ticket": "$400.000",
    "date": date2,
    "hour": "11:00 pm",
    "venue_id": venue_objeto.id,
}
show_objeto2 = organizer.create_show(show2)

date_str3 = "2021-03-12"
year = int(date_str3[0:4])
month = int(date_str3[5:7])
day = int(date_str3[8:10])
date3 = datetime.datetime(year, month, day, 0, 0, 0)
show3 = {
    "name_show": "script 2 - show3 2021-03-12 en 4 dias Rock Bogotá",
    "status_show": "en proceso",
    "price_ticket": "$100.000",
    "date": date3,
    "hour": "12:00 am",
    "venue_id": venue_objeto.id,
}
show_objeto3 = organizer.create_show(show3)
# ShowArtist union artista y shows
show_artist = ShowArtist(
    artist_id=artista_objeto.id,
    show_id=show_objeto.id
)
# tengo dudas de que esta clase tenga este metodo
show_artist.save()

show_artist2 = ShowArtist(
    artist_id=artista_objeto2.id,
    show_id=show_objeto2.id
)
# tengo dudas de que esta clase tenga este metodo
show_artist2.save()

show_artist3 = ShowArtist(
    artist_id=artista_objeto3.id,
    show_id=show_objeto3.id
)
# tengo dudas de que esta clase tenga este metodo
show_artist3.save()

# filtrando shows y artistas :D
# print(show_artist2.artists)  # artista olivia
# print(show_artist.artists)  # artista togres del norte
#print('----->')
#pprint(show_objeto.artists())

# deberia sacar al artista tigres del norte