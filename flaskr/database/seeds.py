from flaskr.database.db import db_session as db
from flaskr.models import Bill, Sponsor
from sqlalchemy import select
from flask.cli import AppGroup
from flask import current_app
from pathlib import Path
import datetime
import click
import csv


def seed_db():
    create_sponsors()
    create_bills()
        

def create_bills():
    bills = db.execute(select(Bill)).first()
    if(not bills):
        filepath = Path("final_data/bills.csv")
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                fa_year, fa_month, fa_day = tuple(row["first_action"].split("-")) if row["first_action"] else tuple([None]*3)
                b = Bill(identifier = row["identifier"],
                        session_identifier = row["session_identifier"],
                        organization_classification = row["organization_classification"],
                        first_action = datetime.date(int(fa_year), int(fa_month), int(fa_day)) if row["first_action"] else None,
                        num_sponsors = int(row["num_sponsors"]),
                        became_law = bool(row["became_law"]),
                        referred_to_committee = bool(row["referred_to_committee"]),
                        committee_passages = int(row["committee_passages"]),
                        passed_first_chamber = bool(row["passed_first_chamber"]),
                        passed_full_legislature = bool(row["passed_full_legislature"])
                )
                sponsor = db.scalar(select(Sponsor).where(Sponsor.name == row["primary_sponsor_1_clean"]))
                b.sponsor_id = sponsor.id
                db.add(b)
            
        db.commit()


def create_sponsors():
    sponsors = db.execute(select(Sponsor)).first()
    if(not sponsors):
        filepath = Path("final_data/sponsors.csv")
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                s = Sponsor(name = row["name"],
                            organization_classification = row["organization_classification"] if row["organization_classification"] else None,
                            donation_count_all = row["donation_count_all"] if row["donation_count_all"] else None,
                            donation_count_L3 = row["donation_count_L3"] if row["donation_count_L3"] else None,
                            total_all = float(row["total_all"]) if row["total_all"] else None,
                            total_L3 = float(row["total_L3"]) if row["total_L3"] else None,
                            pct_c_above_all = float(row["pct_c_above_all"]) if row["pct_c_above_all"] else None,
                            pct_c_above_L3 = float(row["pct_c_above_L3"]) if row["pct_c_above_L3"] else None,
                            avg_donation_all = float(row["avg_donation_all"]) if row["avg_donation_all"] else None,
                            avg_donation_L3 = float(row["avg_donation_L3"]) if row["avg_donation_L3"] else None,
                            amt_allcond_all= float(row["amt_allcond_all"]) if row["amt_allcond_all"] else None,
                            amt_allcond_L3 = float(row["amt_allcond_L3"]) if row["amt_allcond_L3"] else None,
                            pct_c_allcond_all = float(row["pct_c_allcond_all"]) if row["pct_c_allcond_all"] else None,
                            pct_c_allcond_L3 = float(row["pct_c_allcond_L3"]) if row["pct_c_allcond_L3"] else None,
                            pct_c_IL_all = float(row["pct_c_IL_all"]) if row["pct_c_IL_all"] else None,
                            pct_c_IL_L3 = float(row["pct_c_IL_L3"]) if row["pct_c_IL_L3"] else None,
                            num_bills = int(row["num_bills"]) if row["num_bills"] else None,
                            pct_bills_passed = float(row["pct_bills_passed"]) if row["pct_bills_passed"] else None,
                            first_donation_year = row["first_donation_year"]  if row["first_donation_year"] else None,
                            effectiveness_score = float(row["effectiveness_score"]) if row["effectiveness_score"] else None

                )
                db.add(s)
        db.commit()


if __name__ == "__main__":
    seed_db()