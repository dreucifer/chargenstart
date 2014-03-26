from flask import render_template
from core.application import app

from vehicle_lookup.views import VehicleLookups
from product.views import Products
from cart.views import Cart

app.register_blueprint(VehicleLookups)
app.register_blueprint(Products)
app.register_blueprint(Cart)

@app.route('/')
def index():
    from product.views import catalog
    catalog = catalog()
    return render_template('index.html', catalog=catalog)
