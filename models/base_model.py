#!/usr/bin/python3
"""
Contains class BaseModel
"""

# imports the require libraries
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from os import getenv

# define the format of the date
time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

# Base is the instance of the ORM SqlAlchemy
Base = declarative_base()


class BaseModel:
    """
    The BaseModel class from which future classes will be derived
        - id : type(string(60)) will be the id of each object
        - created_at : type(datetime) will be the date of a object is create
        - update_at : type(datetime) will be the date of a object is update
    """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        # if the key is equal to class ignore and continue
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            # give the values of each key in the kwargs dictionary
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, time_fmt)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, time_fmt)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.to_dict())

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        # push into a db the new object
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """returns a dictionary containing all keys/values of the instance"""
        # create a copy of the dictionary
        new_dict = self.__dict__.copy()
        # give isoformat for the keys of dates
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        if '_password' in new_dict:
            new_dict['password'] = new_dict['_password']
            new_dict.pop('_password', None)
        if 'amenities' in new_dict:
            new_dict.pop('amenities', None)
        if 'reviews' in new_dict:
            new_dict.pop('reviews', None)
        # if a key '_sa_instance_state' exists delete of the new_dict
        new_dict.pop('_sa_instance_state', None)
        # delete the pwd key in the dictionary
        if not save_to_disk:
            new_dict.pop('password', None)
        return new_dict

    def delete(self):
        """Delete current instance from storage by calling its delete method"""
        models.storage.delete(self)
