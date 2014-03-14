from flask import render_template
from core import app
from vehicle_lookup.views import lookup

@app.route('/')
def index():
    vlookup = lookup()
    return render_template('index.html', lookup = vlookup)
