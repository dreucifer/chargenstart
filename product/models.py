""" @todo: Docstring """
from flask import url_for, Markup
import re
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from satchless.item import Item
from prices import Price
import database as db

class Category(db.Base):
    __tablename__ = 'categories'

    id_ = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id_'))
    children = relationship('Category',
            cascade="all, delete-orphan",
            backref=backref('parent', remote_side=[id_]))
    name = Column(String)
    slug = Column(String, index=True)
    description = Column(Text)

    def __init__(self, parent=None):
        self.parent = parent

    def __repr__(self):
        return "Category(name=%r, id=%r, parent_id=%r)" % \
                (self.name, self.id_, self.parent_id)

    def dump(self, _indent=0):
        return "\t" * _indent + repr(self) + \
                "\n" + \
                "".join([c.dump(_indent + 1)
                        for c in self.children])

    @property
    def html(self):
        rval = """\
    <ul>
        <li>
            {0}
            {1}
        </li>
    </ul>""".format(unicode(self),
            "\n".join([child.html
                for child in self.children]))
        return rval


    def __unicode__(self):
        return self.name

class Product(db.Base, Item):
    """ @todo: Docstring """
    __tablename__ = 'products'

    id_ = Column(Integer, primary_key=True)
    number = Column(String)
    name = Column(String)
    price = Column(Float)
    cost = Column(Float)
    weight = Column(Float)
    description = Column(Text)
    long_description = Column(Text)
    image_path = Column(String)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """ @todo: Docstring """
        return url_for('product.details',
                slug=self.get_slug(), product_id=self.id_)

    def get_slug(self):
        """ @todo: Docstring """
        value = " ".join([self.number, self.name]).decode('utf-8', 'ignore')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return Markup(re.sub(r'[-\s]+', '-', value))

    def get_formatted_price(self, price=None):
        """ @todo: Docstring """
        if price is None:
            price = self.get_price()
        return "$%.2f %s" % (price.gross, price.currency or 'USD')

    def get_price_per_item(self, **kwargs):
        """ @todo: Docstring """
        return Price(self.price)

    def get_weight(self):
        """ @todo: Docstring """
        return self.weight
