from flaskr.database.db import db_session as db
from flaskr.models import Bill, Sponsor
from flask.cli import AppGroup
from flask import current_app
from pathlib import Path
import click
import csv


def seed_db():
    create_bills()
        

def create_bills():
    filepath = Path("final_data/bills.csv")
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for rows in reader:
            b = Bill(title=rows["title"],session_identifier=rows["session_identifer"],
                    organization_classification=rows["organization_classification"])
            db.add(b)
        
    db.commit()


def create_sponsors():
    pass


if __name__ == "__main__":
    seed_db()