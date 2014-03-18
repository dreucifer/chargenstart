from core import admin
import core.database as db
from products.models import Product
from flask.ext.admin.contrib.sqla import ModelView

admin.add_view(ModelView(Product, db.session))
