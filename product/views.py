""" @todo """
from flask import render_template, request, flash, session, Blueprint
from product.models import Product
from cart.forms import AddToCartForm
from product.utils import get_or_404, first_or_abort, get_for_page
from cart import ShoppingCart, SessionCart

Products = Blueprint('products', __name__, url_prefix='/parts',
        template_folder='templates', static_folder='static')

import product.admin

PER_PAGE = 10

@Products.route('/', methods=['POST', 'GET'])
def index():
    """ @todo """
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('products.html', cart=cart,
            catalog=catalog_page(1))

@Products.route('/catalog/', defaults={'page_number': 1})
@Products.route('/catalog/page/<int:page_number>')
def catalog(page_number):
    cat_page = catalog_page(page_number)
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('catalog.html', cart=cart, catalog_page=cat_page)

def catalog_page(page_number):
    """ @todo """
    pagination = get_for_page(Product.query, page_number, per_page=10)
    return render_template('_catalog.html', pagination=pagination)

@Products.route('/info/<product_id>', methods=['GET', 'POST'])
def details(product_id):
    """ @todo """
    product = get_or_404(Product, product_id)
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(request.form, product=product, cart=cart, product_id=product.id_)

    return render_template('details.html', product=product, form=form, cart=cart)
