from sqlalchemy import Column, Integer, String
from flaskr.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'
    
class Bill():
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

class Sponsors():
    __tablename__ = "sponsors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String (50), unique=False)
    last_name = Column(String(50), unique=False)

