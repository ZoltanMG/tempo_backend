from models import storage
from models.city import City

bogota = storage.session.query(City).filter_by(city_name="Bogotá").first()
bogota2 = storage.session.query(City).filter_by(city_name="Bogotá").first()
print(bogota == bogota2)
print(bogota is bogota2)
