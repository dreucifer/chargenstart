from sqlalchemy import create_engine, MetaData, Table, distinct
from sqlalchemy.engine import reflection
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///products.db')
metadata = MetaData()
session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def db_create():
    import products.models
    Base.metadata.create_all(engine)
