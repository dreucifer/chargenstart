from flask import Blueprint

Products = Blueprint('products', __name__, url_prefix='/parts',
        template_folder='vehicle_lookup/templates', static_folder='vehicle_lookup/static')

import product.views
import product.admin
