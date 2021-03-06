from flask import render_template, request, session
from core.application import app
import database as db

from vehicle_lookup.views import VehicleLookups
from product.views import Products
from cart.views import Cart
from cart import ShoppingCart, SessionCart

app.register_blueprint(VehicleLookups)
app.register_blueprint(Products)
app.register_blueprint(Cart)

@app.before_request
def before_request():
    try:
        cart_data = session['cart']
        shoppingcart = SessionCart.from_storage(cart_data)
    except KeyError:
        shoppingcart = SessionCart()
    setattr(request, 'cart', shoppingcart)

@app.after_request
def after_request(response):
    if hasattr(request, 'cart') and request.cart.modified:
        request.cart.modified = False
        to_session = request.cart.serialize
        session['cart'] = to_session
    return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
    from product.views import _catalog_page
    shoppingcart = ShoppingCart.for_session_cart(request.cart)
    catalog = _catalog_page(1)
    return render_template('index.html', catalog=catalog, cart=shoppingcart)
