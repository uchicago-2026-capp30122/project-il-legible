import sqlite3
import click
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from sqlalchemy import create_engine


engine = create_engine('sqlite:///instance/flaskr.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import flaskr.models
    Base.metadata.create_all(bind=engine)


def init_app(app):
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)


def shutdown_session(exception=None):
        db_session.remove()


def seed_db():
    from flaskr.models import Bill, Sponsor
    for i in range(10, 20):
        b = Bill(f"Test Bill {i}")
        s = Sponsor(f"Test Sponsor {i}")

        db_session.add(b)
        db_session.add(s)

    db_session.commit()

@click.command('seed-db')
def seed_db_command():
    """Add test data to the database"""
    seed_db()
    click.echo('Seeded the database with test data')

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

