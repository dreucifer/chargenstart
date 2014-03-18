import csv
import codecs
import functools
import core.database as db
from vehicle_lookup.models import Year, Make, Model, Type, Engine, ModelYearEngine

def get_or_create(session, obclass, **kwargs):
    result = obclass.query.filter_by(**kwargs).first()
    if not result:
        result = obclass(**kwargs)
        session.add(result)
    return result

def import_data(data_filename):
    with open(data_filename) as data_file:
        data_reader = csv.reader(data_file, delimiter=",")
        for row in data_reader:
            year, make, model = row
            year = get_or_create(db.session,
                    Year, year = int(year.decode('ascii', 'ignore')))
            make = get_or_create(db.session,
                    Make, name = make.decode('ascii', 'ignore'))
            model = get_or_create(db.session, Model,
                    name = model.decode('ascii', 'ignore'))
            model.make = make
            db.session.commit()
            print ", ".join([str(year.year), make.name, model.name])

def importer(filename='import.csv'):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with open(filename) as open_file:
                results = []
                file_reader = csv.DictReader(open_file)
                i = 0
                for row in file_reader:
                    ret = func(row)
                    results.append(ret)
                    if i > 20:
                        db.session.commit()
                        i = 0
                    i = i + 1
            return results
        return inner
    return decorator

@importer(filename='makes.csv')
def import_makes(row):
    print "Imported {0}".format(row['Name'])
    return get_or_create(db.session,
            Make, name = row['Name'])

@importer(filename='types.csv')
def import_types(row):
    print "imported {0} {1}".format(row['makeName'], row['Name'])
    make = Make.query.filter_by(name = row['makeName'])
    vtype = get_or_create(db.session, Type, name = row['Name'])
    make.types.append(vtype)
    return vtype

@importer(filename='models.csv')
def import_models(row):
    with db.session.no_autoflush:
        make = Make.query.filter_by(name = row['makeName']).first()
        vtype = make.types.filter_by(name = row['typeName']).first()
        model = get_or_create(db.session,
                Model, name = row['Name'],
                make = make,
                type_ = vtype)
        print "Added {0} {1} {2}".format(make.name, vtype.name, model.name)
    return model

@importer(filename='years.csv')
def import_years(row):
    make = Make.query.filter_by(name = row['makeName']).first()
    vtype = make.types.filter_by(name = row['typeName']).first()
    model = Model.query.filter_by(
            name = row['modelName'],
            make = make,
            type_=vtype).first()
    year = get_or_create(db.session, Year, name = row['Name'])
    if year not in model.years:
        model.years.append(year)
    print "Added {0} {1} {2}".format(year.name, make.name, model.name)
    return year

@importer(filename='engines.csv')
def import_engines(row):
    make = Make.query.filter_by(name = row['makeName']).first()
    if not make:
        print "[ERROR] Couldn't find %s" % row['makeName']
        return None
    vtype = make.types.filter_by(name = row['typeName']).first()
    model = Model.query.filter_by(
            name = row['modelName'],
            make = make,
            type_ = vtype).first()
    year = model.years.filter_by(name = row['yearName']).first()
    engine = get_or_create(
            db.session,
            Engine, name = row['Name'].encode('ascii', 'ignore'))
    modelyearengine = get_or_create(
            db.session,
            ModelYearEngine,
            engine = engine,
            model = model,
            year = year)
    model.engines.append(modelyearengine)
    print "Added {0} {1} {2} {3}".format(year.name, make.name, model.name, engine.name)
    return engine


def get_makes():
    for make in Make.query.order_by('name').all():
        yield make.serialize

def get_types(make):
    make = Make.query.get(make)
    for vtype in make.types.order_by('name'):
        yield vtype.serialize

def get_models(make, vtype):
    make = Make.query.get(make)
    vtype = Type.query.get(vtype)
    models = Model.query.filter_by(
            make = make, type_ = vtype).order_by('name').all()
    for model in models:
        yield model.serialize

def get_years(model):
    model = Model.query.get(model)
    years = model.years
    for year in years.order_by('name').all():
        yield year.serialize

def get_engines(model, year):
    pass
