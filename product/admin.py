from flask.ext.admin.contrib.sqla import ModelView
import database as db
from product.models import Product, Category
from core.application import admin

admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Category, db.session))
