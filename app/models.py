from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Sponsor(db.Model):
    __tablename__ = "sponsors"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True)
    organization_classification: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    donation_count_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    donation_count_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    total_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    total_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_above_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_above_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    avg_donation_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    avg_donation_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    amt_allcond_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    amt_allcond_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_allcond_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_allcond_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_IL_all: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    pct_c_IL_L3: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    num_bills: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    pct_bills_passed: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    first_donation_year: so.Mapped[Optional[str]] = so.mapped_column(sa.String(4))
    effectiveness_score: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    bills: so.WriteOnlyMapped[Optional['Bill']] = so.relationship(back_populates='sponsor')    

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

    def __repr__(self):
        return '<Sponsor {}>'.format(self.name)
    

class Bill(db.Model):
    __tablename__ = "bills"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    identifier: so.Mapped[str] = so.mapped_column(sa.String(20))
    session_identifier: so.Mapped[Optional[str]] =  so.mapped_column(sa.String(20))
    organization_classification: so.Mapped[Optional[str]] =  so.mapped_column(sa.String(20))
    first_action: so.Mapped[Optional[str]] = so.mapped_column(sa.Date)
    num_sponsors: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    became_law: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean)
    referred_to_committee: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean)
    committee_passages: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    passed_first_chamber: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean)
    passed_full_legislature: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean)

    sponsor_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(Sponsor.id), index=True)
    sponsor: so.Mapped[Sponsor] = so.relationship(back_populates='bills')


    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}


    def __repr__(self):
        return '<Bill {}>'.format(self.identifier)
