from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flaskr.database.db import Base

class Bill(Base):

    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    session_identifer = Column(String(20))
    organization_classification = Column(String(20))
    abstract = Column(Text)
    first_action = Column(Date)
    sponsor_id = Column(Integer, ForeignKey('sponsors.id'))
    num_sponsors = Column(Integer)
    became_law = Column(Boolean)
    committee_passages = Column(Integer)
    passed_first_chamber = Column(Boolean)
    passed_full_legislature = Column(Boolean)

    def __init__(self, title, session_identifier=None, organization_classification=None,
                 abstract=None, first_action=None, sponsor_id=None, num_sponsors=None,
                 became_law=None, committee_passages=None, passed_first_chamber=None,
                 passed_full_legislature=None):
        self.title = title
        self.session_identifer = session_identifier
        self.organization_classification = organization_classification
        self.abstract = abstract
        self.first_action = first_action
        self.sponsor_id = sponsor_id
        self.num_sponsors = num_sponsors
        self.became_law = became_law
        self.committee_passages = committee_passages
        self.passed_first_chamber = passed_first_chamber
        self.passed_full_legislature = passed_full_legislature


class Sponsor(Base):

    __tablename__ = 'sponsors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String (50), unique=False)
    last_name = Column(String(50), unique=False)
    bills = relationship('Bill', backref='sponsor', lazy='dynamic')
    

    def __init__(self, name=None):
        self.first_name= name

