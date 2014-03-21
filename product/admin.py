from flask.ext.admin.contrib.sqla import ModelView
import database as db
from product.models import Product
from core import admin

admin.add_view(ModelView(Product, db.session))
