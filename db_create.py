#!/usr/bin/env python
from vehicle_lookup.database import db_create as db_create_vl
from products.database import db_create as db_create_prod

db_create_vl()
db_create_prod()
