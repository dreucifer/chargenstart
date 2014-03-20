from core import admin
import core.database as db
from vehicle_lookup.models import Model, Make, Type, Year, Engine, ModelYearEngine, Vehicle
from flask.ext.admin.contrib.sqla import ModelView

class MyModelAdmin(ModelView):
    column_searchable_list = (Model.name,)

admin.add_view(ModelView(Make, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(MyModelAdmin(Model, db.session))
admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Engine, db.session))
admin.add_view(ModelView(ModelYearEngine, db.session))
admin.add_view(ModelView(Vehicle, db.session))
