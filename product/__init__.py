from flask import Blueprint

Products = Blueprint('products', __name__, url_prefix='/parts',
        template_folder='templates', static_folder='static')

import product.views
import product.admin
