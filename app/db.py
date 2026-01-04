# db.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

load_dotenv()

# DATABASE_URL = os.getenv('DATABASE_URL')


# Initialize database after flask has created the app
ENGINE = None
db_session = scoped_session(sessionmaker())

def init_db(app):
    global ENGINE
    DATABASE_URL = app.config['SQLALCHEMY_DATABASE_URI']
    ENGINE = create_engine(DATABASE_URL, echo=app.config.get('SQL_ALCHEMY_ECHO', False))

    db_session.configure(bind=ENGINE)

    # Create tables for local development
    if app.config.get('CREATE_TABLES', False):
        Base.metadata.create_all(ENGINE)