""" @todo: Docstring """
from flask import Markup, url_for
import re
from sqlalchemy import Column, Integer, String, Float, Text
from satchless.item import Item
from prices import Price
import database as db

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

    def get_formatted_price(self):
        """ @todo: Docstring """
        price = self.get_price()
        return "$%.2f %s" % (price.gross, price.currency or 'USD')

    def get_price_per_item(self, **kwargs):
        """ @todo: Docstring """
        return Price(self.price)

    def get_weight(self):
        """ @todo: Docstring """
        return self.weight
