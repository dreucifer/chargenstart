from flask import Blueprint, request, session, redirect, url_for, render_template
from cart import SessionCart, ShoppingCart
from cart.forms import AddToCartForm
from product.utils import get_or_404
from product.models import Product

Cart = Blueprint('cart', __name__, url_prefix='/cart',
                 template_folder='templates',
                 static_folder='static')

import cart.admin

@Cart.before_app_request
def before_app_request():
    try:
        cart_data = session['cart']
        shoppingcart = SessionCart.from_storage(cart_data)
    except KeyError:
        shoppingcart = SessionCart()
    setattr(request, 'cart', shoppingcart)

@Cart.after_app_request
def after_app_request(response):
    if hasattr(request, 'cart'):
        to_session = request.cart.serialize
        session['cart'] = to_session
    return response

@Cart.route('/')
def index():
    shoppingcart = ShoppingCart.for_session_cart(request.cart)
    return render_template('cart.html', cart=shoppingcart)

@Cart.route('/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = get_or_404(Product, product_id)
    shoppingcart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(request.form, product=product, cart=shoppingcart)
    if form.validate():
        form.save()
    return redirect(url_for('.index'))
