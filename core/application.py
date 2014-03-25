from flask import Flask, redirect, url_for
from flask.ext.admin import Admin

app = Flask('chargenstart')
app.config.from_object('core.config')

admin = Admin(app)

if not app.debug:
    import logging
    file_handler = logging.FileHandler(filename="log.txt")
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

import core.views
