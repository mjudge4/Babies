# Provides objects and variables to manipulate the project runtime environment

import sys

# Object relational mapping
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

# To create instance of the class called declarative base to import SQL Alchemy Features
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

# Create instance
Base = declarative_base()



class Offering(Base):
    __tablename__ = 'offering'

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    date = Column(String(300), nullable=False)

    @property
    def serialize(self):
        #Return objects in serializable form
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,

        }



class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(300), nullable=False)
    offering_id = Column(Integer, ForeignKey('offering.id'))
    offering = relationship('Offering')

    @property
    def serialize(self):
        # Return objects in serializable form
        return {
            'id': self.id,
            'tag_name': self.tag_name,

        }


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    body = Column(String(1000), nullable=False)
    offering_id = Column(Integer, ForeignKey('offering.id'))
    offering = relationship('Offering')

    @property
    def serialize(self):
        # Return objects in serializable form
        return {
            'id': self.id,
            'body': self.body,

        }



# Engine instance with a sqllite database
engine = create_engine('sqlite:///offerings.db')

# Goes into database and creates the tables
Base.metadata.create_all(engine)