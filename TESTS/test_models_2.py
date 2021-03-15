#!/usr/bin/python3

from models import storage
from models.city import City
from models.venue import Venue
from models.show import Show
from models.artist import Artist
from models.organizer import Organizer
from werkzeug.security import generate_password_hash, check_password_hash

# Create city
city = City(city_name='Bogota', country_name="Colombia")
city.save()
pwd = 'pwd'
pwd_md5 = generate_password_hash(pwd)
organizer = Organizer(names_organizer="Rock al Parque",
                      email="rock_4@alparque.com", pwd=pwd_md5, social="aqui.com")
organizer.save()
# create venue
venue = {"city_id": city.id, "venue_name": "venue_1",
         "email": "asilo@mail.com", "address": "Calle del cartucho", "capacity": 150}
venue_2 = {"city_id": city.id, "venue_name": "venue_2",
           "email": "asilo_2@mail.com", "address": "Calle del cartucho 2", "capacity": 250}
obj_venue = organizer.create_venue(venue)
obj_venue_2 = organizer.create_venue(venue_2)

# Create artist
artist = {"name_show": "los borrachos", "artist_name": "Monkeys",
          "genre_artist": "Funk", "email": "monkey@mail.com"}
obj_artist = organizer.create_artist(artist)
# create show
# print(type(venue))
show = {"name_show": "show", "venue_id": obj_venue_2.id, "price_tikets": 25000,
        "status_show": "en curso", "date_show": "today", "artist_id": obj_artist.id}
show_2 = {"name_show": "show 2", "venue_id": obj_venue.id, "price_tikets": 35000,
          "status_show": "en curso", "date_show": "today", "artist_id": obj_artist.id}
show_3 = {"name_show": "show 3", "venue_id": obj_venue_2.id, "price_tikets": 25000,
          "status_show": "en curso", "date_show": "today", "artist_id": obj_artist.id}
show_4 = {"name_show": "show 4", "venue_id": obj_venue.id, "price_tikets": 20000,
          "status_show": "en curso", "date_show": "today", "artist_id": obj_artist.id}
obj_show = organizer.create_show(show)
obj_show_2 = organizer.create_show(show_2)
obj_show_3 = organizer.create_show(show_3)
obj_show_4 = organizer.create_show(show_4)
print(organizer)
# print(obj_venue)
# print(obj_show)
# print(obj_artist)
