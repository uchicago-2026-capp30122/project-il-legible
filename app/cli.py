from flask import Blueprint
from app.database import seeds
from app import db as database
import click

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def db():
    """Additional database commands."""
    pass


@db.command()
def seed():
    """Fill the database with data"""
    seeds.seed_db()
    click.echo("Records inserted into database.")


@db.command()
def create_tables():
    """Create tables in the database"""
    database.create_all()
    click.echo("All tables added to the database")


@db.command()
def drop_tables():
    """Drop the database if it exists"""
    database.drop_all()
    click.echo("All tables dropped from database")
