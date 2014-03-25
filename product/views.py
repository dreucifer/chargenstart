""" @todo """
from flask import render_template, request, flash, session
from product import Products
from product.models import Product
from cart.forms import AddToCartForm
from product.utils import get_or_404, first_or_abort
from cart import ShoppingCart, SessionCart

@Products.route('/', methods=['POST', 'GET'])
def index():
    """ @todo """
    cart = ShoppingCart.for_session_cart(request.cart)
    return render_template('products.html', cart=cart)

@Products.route('/info/<product_id>', methods=['GET', 'POST'])
def details(product_id):
    """ @todo """
    product = get_or_404(Product, product_id)
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm(product=product, cart=cart)

    if form.validate():
        form.save()
    return render_template('details.html', product=product, form=form, cart=cart)
