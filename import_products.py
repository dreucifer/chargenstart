#!/usr/bin/env python
# encoding: utf-8

import functools
import csv
import database as db
from product.models import Product

def get_or_create(session, obclass, **kwargs):
    result = obclass.query.filter_by(**kwargs).first()
    if not result:
        result = obclass(**kwargs)
        session.add(result)
    return result

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

@importer(filename='products.csv')
def import_products(row):
    print "Importing part # {0}".format(row['PartNumber'])
    try:
        rv = get_or_create(db.session, Product,
                number=row['PartNumber'],
                name=row['Name'].decode('ascii', 'ignore'),
                price=row['CustomerPrice'],
                cost=row['StoreCost'],
                weight=row['WeightMajor'],
                description=row['ShortDescription'].decode('ascii', 'ignore'))
    except KeyError:
        return None
    return rv

if __name__ == '__main__':
    import_products()
