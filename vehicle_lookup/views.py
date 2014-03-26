""" This holds the view logic and URL information """
from flask import Blueprint, redirect, url_for, request, render_template, current_app
from wtforms.fields import SelectField
from vehicle_lookup.models import Year, Make, Model, Engine, Type, ModelYearEngine
from vehicle_lookup.helpers import (
        get_or_create, get_makes, get_types,
        get_models, get_years, get_engines)
import database as db
import flask.json as json

VehicleLookups = Blueprint('vehicle_lookup', __name__, url_prefix='/vl',
        template_folder='templates', static_folder='vehicle_lookup/static')

import vehicle_lookup.admin

@VehicleLookups.route('/lookup')
def lookup():
    """ Render the basic template """
    return render_template('lookup.html')

@VehicleLookups.route('/', methods=['POST','GET'])
def index():
    status = 'Failure'
    data = []

    make = request.values.get('make', None, type=str)
    vtype = request.values.get('type', None, type=str)
    model = request.values.get('model', None, type=str)
    year = request.values.get('year', None, type=str)
    engine = request.values.get('engine', None, type=str)

    if make:
        if vtype:
            data.append('crumps')
        else:
            data = data + list(get_types(make))
    else:
        data = data + list(get_makes())

    return json.dumps({ 'status': status, 'data': data })

@VehicleLookups.route('/vlmake', methods=['POST', 'GET'])
def vlmake():
    status = 'Success'
    data = list(get_makes())
    return json.dumps({ 'status': status, 'data': data })

@VehicleLookups.route('/vltype', methods=['POST', 'GET'])
def vltype():
    make = request.values.get('make', None, type=int)
    data = []
    if make:
        status = 'Success'
        data = list(get_types(make))
    else:
        status = 'Failure'
    return json.dumps({ 'status': status, 'data': data })

@VehicleLookups.route('/vlmodel', methods=['POST', 'GET'])
def vlmodel():
    data = []
    make = request.values.get('make', None, type=int)
    vtype = request.values.get('type', None, type=str)
    if make and vtype:
        status = 'Success'
        data = list(get_models(make, vtype))
    else:
        status = 'Failure'
    return json.dumps({'status': status, 'data': data})

@VehicleLookups.route('/vlyear', methods=['POST', 'GET'])
def vlyear():
    data = []
    model = request.values.get('model', None, type=int)
    if model:
        status = 'Success'
        data = list(get_years(model))
    else:
        status = 'Failure'

    return json.dumps({'status': status, 'data': data})

@VehicleLookups.route('/parts')
@VehicleLookups.route('/pt')
def get_parts():
    from uuid import UUID
    callback = request.args.get('callback')
    status = 'Failure'
    data = []
    vehicle_guid = request.args.get('guid')

    vehicle = Vehicle.query.filter_by(guid = UUID(vehicle_guid)).first()
    if vehicle:
        parts = vehicle.parts.all()
        if parts:
            status = 'Success'
            data = [part.serialize for part in vehicle.parts.all()]

    return "{0}({1})".format(callback,
            json.dumps({ 'status': status, 'data': data }))
