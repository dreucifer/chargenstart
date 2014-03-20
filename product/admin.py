from core import admin
import core.database as db
from product.models import Product
from flask.ext.admin.contrib.sqla import ModelView

admin.add_view(ModelView(Product, db.session))
