from flask import render_template
from core.application import app
from vehicle_lookup.views import lookup

from vehicle_lookup import VehicleLookups
from product import Products
from cart import Cart

app.register_blueprint(VehicleLookups)
app.register_blueprint(Products)
app.register_blueprint(Cart)

@app.route('/')
def index():
    vlookup = lookup()
    return render_template('index.html', lookup=vlookup)
