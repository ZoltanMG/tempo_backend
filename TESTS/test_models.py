#!/usr/bin/python3

from models import storage
from models.city import City
from models.venue import Venue
from models.show import Show
from models.artist import Artist
from models.organizer import Organizer
#Create city
city = City(city_name='Bogota', country_name="Colombia")
city.save()

organizer = Organizer(names_organizer="Zoltan", email="Zoltan@tempo.com", pwd="pwd", social="aqui.com")
organizer.save()
#create venue
venue = {"city_id": city.id, "venue_name": "Asilo", "email": "asilo@mail.com", "address": "Calle del cartucho", "capacity": 150}
obj_venue = organizer.create_venue(venue)

#Create artist
artist = {"name_show": "los borrachos", "artist_name": "Monkeys", "genre_artist": "Funk", "email": "monkey@mail.com"}
obj_artist = organizer.create_artist(artist)
#create show
#print(type(venue))
show = {"venue_id": obj_venue.id, "price_tikets": 25000, "status_show": "en curso","date_show": "today", "artist_id": obj_artist.id}
obj_show = organizer.create_show(show)
print(organizer)
print(obj_venue)
print(obj_show)
print(obj_artist)
