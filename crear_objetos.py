#!/usr/bin/python3
"""
script that starts dummy data into a db tempo
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
medellin = storage.session.query(City).filter_by(city_name="Medellín").first()


# Organizer
pwd = 'pwd'
pwd_md5 = generate_password_hash(pwd)
organizer = Organizer(names_organizer="Rock al Parque",
                      email="rock_4@alparque.com", pwd=pwd_md5)
organizer.save()

#  Social newtwork organizer
social_organizer = SocialOrganizer(
    organizer_id=organizer.id,
    link="facebook.com/rock-al-parque",
    description="Facebook"
)
social_organizer.save()

# Organizer2
pwd2 = 'pwd2'
pwd_md5 = generate_password_hash(pwd2)
organizer2 = Organizer(names_organizer="Bar quilla",
                       email="rock_2@alparque.com", pwd=pwd_md5)
organizer2.save()

# Social newtwork organizer2
social_organizer2 = SocialOrganizer(
    organizer_id=organizer2.id,
    link="facebook.com/rock2-al-parque",
    description="Facebook2"
)
social_organizer2.save()


# Venues
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
venue_objeto = organizer2.create_venue(venue)

venue2 = {
    "city_id": medellin.id,
    "venue_name": "LOS TINTEROS",
    "address": "Comuna 13",
    "phone": "376737326",
    "capacity": "200",
    "latitude": "8.90",
    "longitude": "0.100",
    "description": "LOS TINTEROS ES UN BAR QUE TE OFRECE MULTIPLES SERVICIOS ESTAMOS UBICADOS A DOS CUADRAS DEL PARQUE DE LAS FLORES :)"
}
venue_objeto2 = organizer.create_venue(venue2)

venue3 = {
    "city_id": bogota.id,
    # "organizer_id": organizer.id,
    "venue_name": "LOS MARTIRES",
    "address": "Calle 40 SUR",
    "phone": "235558748734",
    "capacity": "350",
    "latitude": "0.89",
    "longitude": "10202.98",
    "description": "LOS MARTIRES ES UN BAR QUE TE OFRECE MULTIPLES SERVICIOS ESTAMOS UBICADOS A DOS CUADRAS DEL PARQUE DE LOS NOVIOS :)"
}
venue_objeto3 = organizer.create_venue(venue3)

# Artists
artista = {
    "artist_name": "tigres del norte",
    "genre_artist": "Norteña"
}
artista_objeto = organizer.create_artist(artista)

artista2 = {
    "artist_name": "metalica",
    "genre_artist": "Metal"
}
artista_objeto2 = organizer.create_artist(artista2)


artista3 = {
    "artist_name": "Olivia Rodrigo",
    "genre_artist": "Pop"
}
artista_objeto3 = organizer.create_artist(artista3)


artista4 = {
    "artist_name": "conchos",
    "genre_artist": "san juanero"
}
artista_objeto4 = organizer.create_artist(artista4)

# Social newtwork artist
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

# Dates
date_str = "2021-04-12"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date = datetime.datetime(year, month, day, 0, 0, 0)


show = {
    "name_show": "show 2021-04-12 en 3 meses Norteña bogotá",
    "status_show": "en curso",
    "price_ticket": "$250.000",
    "date": date,
    "hour": "8:00 pm",
    "description_show": "test descripcion shows",
    "venue_id": venue_objeto.id,
}
show_objeto = organizer2.create_show(show)

date_str = "2021-03-09"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date5 = datetime.datetime(year, month, day, 0, 0, 0)

show5 = {
    "name_show": "show5 hoy Norteña bogota",
    "status_show": "en curso",
    "price_ticket": "$250.000",
    "date": date5,
    "hour": "8:00 pm",
    "description_show": "test descripcion shows",
    "venue_id": venue_objeto.id,
}
show_objeto5 = organizer2.create_show(show5)

date_str = "2021-06-01"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date2 = datetime.datetime(year, month, day, 0, 0, 0)


show2 = {
    "name_show": "show2 dentro de 3 meses Metal Medellín",
    "status_show": "cancelado",
    "price_ticket": "$400.000",
    "date": date2,
    "hour": "11:00 pm",
    "description_show": "test descripcion shows",
    "venue_id": venue_objeto2.id,
}
show_objeto2 = organizer.create_show(show2)

date_str = "2021-04-09"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date3 = datetime.datetime(year, month, day, 0, 0, 0)


show3 = {
    "name_show": "show3 dentro de  1 mes Pop Bogotá",
    "status_show": "en proceso",
    "price_ticket": "$100.000",
    "date": date3,
    "hour": "12:00 am",
    "description_show": "test descripcion shows",
    "venue_id": venue_objeto3.id,
}
show_objeto3 = organizer.create_show(show3)

date_str = "2021-04-09"
year = int(date_str[0:4])
month = int(date_str[5:7])
day = int(date_str[8:10])
date4 = datetime.datetime(year, month, day, 0, 0, 0)

show4 = {
    "name_show": "show4 en medellin conchos, san juanero",
    "status_show": "cancelado",
    "price_ticket": "$300.000",
    "date": date4,
    "hour": "2:00 pm",
    "description_show": "test descripcion shows",
    "venue_id": venue_objeto2.id,
}
show_objeto4 = organizer2.create_show(show4)

# ShowArtist joins artists and shows
show_artist = ShowArtist(
    artist_id=artista_objeto.id,
    show_id=show_objeto.id
)
show_artist.save()

show_artist2 = ShowArtist(
    artist_id=artista_objeto2.id,
    show_id=show_objeto2.id
)
show_artist2.save()

show_artist3 = ShowArtist(
    artist_id=artista_objeto3.id,
    show_id=show_objeto3.id
)
show_artist3.save()


show_artist4 = ShowArtist(
    artist_id=artista_objeto4.id,
    show_id=show_objeto4.id
)
show_artist4.save()

show_artist5 = ShowArtist(
    artist_id=artista_objeto.id,
    show_id=show_objeto5.id
)
show_artist5.save()
