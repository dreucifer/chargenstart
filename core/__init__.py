from flask import Flask, redirect, url_for
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from vehicle_lookup import vlookup

app = Flask('chargenstart')
app.register_blueprint(vlookup)
app.config.from_object('core.config')

admin = Admin(app)
import vehicle_lookup.admin
import products.admin

if not app.debug:
    import logging
    file_handler = logging.FileHandler(filename="log.txt")
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

import core.views
