from sqlalchemy import Column, Integer, Float, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flaskr.database.db import Base

class Bill(Base):

    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    identifier = Column(String(20))
    session_identifier = Column(String(20))
    organization_classification = Column(String(20))
    first_action = Column(Date)
    sponsor_id = Column(Integer, ForeignKey('sponsors.id'))
    num_sponsors = Column(Integer)
    became_law = Column(Boolean)
    referred_to_committee = Column(Boolean)
    committee_passages = Column(Integer)
    passed_first_chamber = Column(Boolean)
    passed_full_legislature = Column(Boolean)

    def __init__(self, identifier, session_identifier=None, organization_classification=None,
                 first_action=None, sponsor_id=None, num_sponsors=None,
                 became_law=None, referred_to_committee=None,
                 committee_passages=None, passed_first_chamber=None,
                 passed_full_legislature=None):
        self.identifier = identifier
        self.sponsor_id = sponsor_id
        self.session_identifier = session_identifier
        self.organization_classification = organization_classification
        self.first_action = first_action
        self.sponsor_id = sponsor_id
        self.num_sponsors = num_sponsors
        self.became_law = became_law
        self.referred_to_committee = referred_to_committee
        self.committee_passages = committee_passages
        self.passed_first_chamber = passed_first_chamber
        self.passed_full_legislature = passed_full_legislature


class Sponsor(Base):

    __tablename__ = 'sponsors'
    id = Column(Integer, primary_key=True)
    name = Column(String (50), unique=False)
    organization_classificaiton = Column(String(20))
    donation_count_all = Column(Integer)
    donation_count_L3 = Column(Integer)
    total_all = Column(Float)
    total_L3 = Column(Float)
    pct_c_above_all = Column(Float)
    pct_c_above_L3 = Column(Float)
    avg_donation_all = Column(Float)
    avg_donation_L3 = Column(Float)
    amt_allcond_all = Column(Float)
    amt_allcond_L3 = Column(Float)
    pct_c_allcond_all = Column(Float)
    pct_c_allcond_L3 = Column(Float)
    pct_c_IL_all = Column(Float)
    pct_c_IL_L3 = Column(Float)
    num_bills = Column(Integer)
    pct_bills_passed = Column(Float)
    first_donation_year = Column(String(4))
    effectiveness_score = Column(Float)
    bills = relationship('Bill', backref='sponsor', lazy='dynamic')
    

    def __init__(self, name, organization_classification=None, donation_count_all=None,
                 donation_count_L3=None, total_all=None, total_L3=None, pct_c_above_all=None,
                 pct_c_above_L3=None, avg_donation_all=None, avg_donation_L3=None,
                 amt_allcond_all=None, amt_allcond_L3=None, pct_c_allcond_all=None,
                 pct_c_allcond_L3=None, pct_c_IL_all=None, pct_c_IL_L3=None, num_bills=None,
                 pct_bills_passed=None, first_donation_year=None, effectiveness_score=None):
        self.name = name
        self.organization_classificaiton = organization_classification
        self.donation_count_all = donation_count_all
        self.donation_count_L3 = donation_count_L3
        self.total_all = total_all
        self.total_L3 = total_L3
        self.pct_c_above_all = pct_c_above_all
        self.pct_c_above_L3 = pct_c_above_L3
        self.avg_donation_all = avg_donation_all
        self.avg_donation_L3 = avg_donation_L3
        self.amt_allcond_all = amt_allcond_all
        self.amt_allcond_L3 = amt_allcond_L3
        self.pct_c_allcond_all = pct_c_allcond_all
        self.pct_c_allcond_L3 = pct_c_allcond_L3
        self.pct_c_IL_all = pct_c_IL_all
        self.pct_c_IL_L3 = pct_c_IL_L3
        self.num_bills = num_bills
        self.pct_bills_passed = pct_bills_passed
        self.first_donation_year = first_donation_year
        self.effectiveness_score = effectiveness_score

