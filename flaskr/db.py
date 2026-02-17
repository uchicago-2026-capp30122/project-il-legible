import sqlite3
from datetime import datetime
import click
from flask import current_app, g, Flask
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# app = Flask(__name__)
DATABASE = 'instance/flaskr.sqlite'

db_config = URL.create(
    "sqlite",
    username="",
    password="",  # plain (unescaped) text
    host="",
    database=DATABASE,
)

engine = create_engine(db_config)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import flaskr.models
    Base.metadata.create_all(bind=engine)


def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)
    

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

