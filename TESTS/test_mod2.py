#!/usr/bin/python3

from models import storage
from models.city import City
from models.venue import Venue
from models.show import Show
from models.artist import Artist
from models.organizer import Organizer
#Create city
organizer = Organizer
city = City(city_name='Cali', country_name="Colombia")
city.save()

#create venue
venue = Venue(city_id=city.id, venue_name="Asilo", email="asilo@mail.com", address="Calle del cartucho", capacity=150)
venue.save()
#create show
show = Show(venue_id=venue.id, price_tikets= 25000)
#Create artist
artist = Artist(artist_name="Ponkeys", genre_artist="Funk", email="ponkey@mail.com")
artist.save()
print(venue)
print(show)
print(artist)
print(show.org_id)
