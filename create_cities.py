#!/usr/bin/python3
from models.city import City

# create cities
city = City(city_name='Bogotá', country_name="Colombia", state="Bogotá DC")
# save city object
city.save()

city2 = City(city_name='Medellín', country_name="Colombia", state="Antioquia")
# save city2 object
city2.save()
