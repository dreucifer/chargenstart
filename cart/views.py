from flask import Blueprint, request, session, redirect, url_for, render_template
from cart import SessionCart, ShoppingCart
from cart.forms import AddToCartForm
from product.utils import get_or_404
from product.models import Product

Cart = Blueprint('cart', __name__, url_prefix='/cart',
                 template_folder='templates',
                 static_folder='static')

import cart.admin

@Cart.route('/')
def index():
    shoppingcart = ShoppingCart.for_session_cart(request.cart)
    return render_template('cart.html', cart=shoppingcart)

@Cart.route('/add', methods=['POST'])
def add_to_cart():
    if request.form:
        try:
            product = get_or_404(Product, request.form['product_id'])
        except KeyError:
            return redirect(request.referrer)
        shoppingcart = ShoppingCart.for_session_cart(request.cart)
        form = AddToCartForm(request.form, product=product, cart=shoppingcart)
        if form.validate():
            form.save()
        return redirect(url_for('.index'))
    return redirect(request.referrer)
