""" @todo """
from flask import render_template, request, flash, session, Blueprint
from product.models import Product
from cart.forms import AddToCartForm
from product.utils import get_or_404, first_or_abort
from cart import ShoppingCart, SessionCart

Products = Blueprint('products', __name__, url_prefix='/parts',
        template_folder='templates', static_folder='static')

import product.admin

@Products.route('/', methods=['POST', 'GET'])
def index():
    """ @todo """
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('products.html', cart=cart, catalog=catalog())

def catalog():
    """ @todo """
    products = Product.query.all()
    return render_template('_catalog.html', products=products)

@Products.route('/info/<product_id>', methods=['GET', 'POST'])
def details(product_id):
    """ @todo """
    product = get_or_404(Product, product_id)
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(request.form, product=product, cart=cart)

    if request.method == 'POST' and form.validate():
        form.save()

    return render_template('details.html', product=product, form=form, cart=cart)
