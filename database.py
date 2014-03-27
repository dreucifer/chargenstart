from sqlalchemy import create_engine, MetaData, Table, distinct
from sqlalchemy.engine import reflection
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///core.db')
metadata = MetaData()
session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def db_create():
    import vehicle_lookup.models
    import product.models
    Base.metadata.create_all(engine)

from math import ceil

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page,
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
            right_edge=2, right_current=5):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
