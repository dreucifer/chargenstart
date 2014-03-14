""" Vehicle Parts Lookup """

from flask import Blueprint

vlookup = Blueprint('vehicle_lookup', __name__, url_prefix='/vl',
        template_folder='templates', static_folder='vehicle_lookup/static')

import vehicle_lookup.views
