from flask import Blueprint

prods = Blueprint('products', __name__, url_prefix='/parts',
        template_folder='templates', static_folder='vehicle_lookup/static')

import products.views
