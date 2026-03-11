import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    db_url = os.environ.get("DATABASE_URL")

    if db_url:
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace(
            "postgres://", "postgresql://"
        )
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            basedir, "instance/app.db"
        )

    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
