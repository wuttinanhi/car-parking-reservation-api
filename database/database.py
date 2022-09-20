"""
    database module
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

engine = create_engine(os.getenv("DATABASE_URI"))
db_session: Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class Base():
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
    Base.metadata.create_all(bind=engine)
