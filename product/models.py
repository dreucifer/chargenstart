from flask import Markup, url_for
import re
from sqlalchemy import Column, Integer, String, Float, Text, PickleType
from satchless.item import Item
from prices import Price
import core.database as db
from core.types import PriceField

class Product(db.Base, Item):
    __tablename__ = 'products'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(PriceField())
    cost = Column(PriceField())
    description = Column(Text)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return url_for('product.details',
                slug=self.get_slug(), product_id=self.id_)

    def get_slug(self):
        value = self.name.decode('utf-8', 'ignore')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return Markup(re.sub(r'[-\s]+', '-', value))

    def get_formatted_price(self, price):
        return "{0} {1}".format(price.gross, price.currency)

    def get_price_per_item(self, **kwargs):
        return self.price
