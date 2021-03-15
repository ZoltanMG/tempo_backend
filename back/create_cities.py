#!/usr/bin/python3
from models.city import City

# Ciudades
city = City(city_name='Bogotá', country_name="Colombia", state="Bogotá DC")
city.save()

city2 = City(city_name='Medellín', country_name="Colombia", state="Antioquia")
city2.save()
