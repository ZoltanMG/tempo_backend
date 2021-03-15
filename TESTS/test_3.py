#!/usr/bin/python3

from models import storage
from models.city import City
from models.venue import Venue
from models.show import Show
from models.artist import Artist
from models.social_organizer import SocialOrganizer
from models.social_artist import SocialArtist
from models.organizer import Organizer
from werkzeug.security import generate_password_hash, check_password_hash

# Create city
city = City(city_name='Bogotá', country_name="Colombia", state="Bogotá DC")
city.save()
pwd = 'pwd'
pwd_md5 = generate_password_hash(pwd)
organizer = Organizer(names_organizer="Rock al Parque",
                      email="rock_1@alparque.com", pwd=pwd_md5)
organizer_2 = Organizer(names_organizer="Rock al Parque",
                      email="rock_2@alparque.com", pwd=pwd_md5)
organizer.save()
organizer_2.save()

# social object
social_1 = SocialOrganizer(organizer_id=organizer.id)
social_1.save()
social_2 = SocialOrganizer(organizer_id=organizer_2.id)
social_2.save()
social_3 = SocialOrganizer(organizer_id=organizer_2.id)
social_3.save()

# create venue
venue = {"city_id": city.id, "venue_name": "venue_1",
         "address": "Calle del cartucho", "capacity": 150, "phone": "23555"}
venue_2 = {"city_id": city.id, "venue_name": "venue_2",
           "address": "Calle del cartucho 2", "capacity": 250, "phone": "23555"}
obj_venue = organizer.create_venue(venue)


# Create artist
artist = {"name_show": "los borrachos", "artist_name": "Monkeys",
          "genre_artist": "Funk"}
obj_artist = organizer.create_artist(artist)
obj_artist_2 = organizer_2.create_artist(artist)

social_2 = SocialArtist(artist_id=obj_artist.id)
social_2.save()
social_3 = SocialArtist(artist_id=obj_artist_2.id)
social_3.save()

# create show
show = {"name_show": "show", "venue_id": obj_venue.id, "price_ticket": 25000,
        "status_show": "en curso", "date": "today", "artist_id": obj_artist.id, "hour": "2pm"}
show_2 = {"name_show": "show 2", "venue_id": obj_venue.id, "price_ticket": 35000,
          "status_show": "en curso", "date": "today", "artist_id": obj_artist.id, "hour": "2pm"}
show_3 = {"name_show": "show 3", "venue_id": obj_venue.id, "price_ticket": 25000,
          "status_show": "en curso", "date": "today", "artist_id": obj_artist.id, "hour": "2pm"}
show_4 = {"name_show": "show 4", "venue_id": obj_venue.id, "price_ticket": 20000,
          "status_show": "en curso", "date": "today", "artist_id": obj_artist.id, "hour": "2pm"}
obj_show = organizer.create_show(show)
obj_show_2 = organizer.create_show(show_2)
obj_show_3 = organizer.create_show(show_3)
obj_show_4 = organizer.create_show(show_4)
