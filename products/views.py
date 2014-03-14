from flask import render_template
from products import prods

@prods.route('/')
def index():
    return render_template('products.html')
