"""
    database module
"""
import os

from env_wrapper import load_env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session

load_env()


def get_engine():
    return create_engine(os.getenv("DATABASE_URI"), echo=False)


engine = get_engine()


def get_db_session() -> Session:
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


db_session: scoped_session = get_db_session()


class Base:
    """
    class for type hint
    """

    query: Query


Base = declarative_base()
Base.query: Query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import car.model
    import chat.model
    import parking_lot.model
    import payment.model
    import reservation.model
    import settings.model
    import user.model

    Base.metadata.create_all(bind=engine)
