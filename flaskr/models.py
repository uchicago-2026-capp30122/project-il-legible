from sqlalchemy import Column, Integer, String
from flaskr.database.db import Base

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    def __init__(self, name=None):
        self.name = name

class Sponsor(Base):
    __tablename__ = 'sponsors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String (50), unique=False)
    last_name = Column(String(50), unique=False)

    def __init__(self, name=None):
        self.first_name= name

