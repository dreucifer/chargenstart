""" @todo """
from flask import render_template
from product import Products
from product.models import Product

@Products.route('/')
def index():
    """ @todo """
    return render_template('products.html')

@Products.route('/info/<product_id>')
def details(product_id):
    """ @todo """
    product = Product.query.get(product_id)
    return render_template('details.html', product=product)
