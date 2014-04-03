""" @todo """
from flask import render_template, request, flash, session, Blueprint, abort
from product.models import Product, Category
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
    cat_page = _catalog_page(1, per_page=10)
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('products.html', cart=cart, catalog=cat_page)

@Products.route('/catalog/', defaults={'page_number': 1})
@Products.route('/catalog/page/<int:page_number>')
def catalog(page_number):
    cat_page = _catalog_page(page_number, per_page=10)
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('catalog.html', cart=cart, catalog_page=cat_page)

@Products.route('/info/<product_id>', methods=['GET', 'POST'])
def details(product_id):
    """ @todo """
    part = get_or_404(Product, product_id)
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(request.form, product=part, cart=cart, product_id=part.id_)

    return render_template('details.html', product=part, form=form, cart=cart)

def _catalog_page(page_number, per_page=20):
    """ @todo """
    pagination = get_for_page(Product.query, page_number, per_page=per_page)
    product_listings = [_product_listing(part) for part in pagination.items]
    return render_template('_catalog.html',
                           pagination=pagination,
                           parts=product_listings)

def _product_listing(part):
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(request.form, product=part,
                         cart=cart, product_id=part.id_)

    return render_template('_product_listing.html', form=form, product=part,
                           cart=cart)
