#!/usr/bin/python3

# import the require libraries
from models.engine.db_storage import DBStorage
# create a instance called storage of the class DBStorage()
storage = DBStorage()
# create correctly the data to save into a db
storage.reload()
