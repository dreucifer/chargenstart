import os
import os.path as op

from flask import url_for, Markup
from flask.ext.admin import form
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy.event import listens_for
import database as db
from product.models import Product, Category
from core.application import admin

file_path = op.join(op.dirname(__file__), '../static')
try:
    os.mkdir(file_path)
except OSError:
    pass

@listens_for(Product, 'after_delete')
def del_image(mapper, connection, target):
    if target.image_path:
        try:
            os.remove(op.join(file_path, target.image_path))
        except OSError:
            pass

class ProductView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ''
        return Markup('<img src="%s">' % url_for('static',
            filename=form.thumbgen_filename(model.image_path)))

    column_formatters = {
            'image_path': _list_thumbnail
            }

    column_searchable_list = ('name', 'number')

    form_extra_fields = {
            'image_path': form.ImageUploadField('Product',
                base_path=file_path,
                thumbnail_size=(100, 100, True))
            }

admin.add_view(ProductView(Product, db.session))
admin.add_view(ModelView(Category, db.session))
