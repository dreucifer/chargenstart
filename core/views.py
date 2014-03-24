from flask import render_template, request, session
from core import app
from cart import ShoppingCart, SessionCart
from vehicle_lookup.views import lookup

@app.route('/')
def index():
    vlookup = lookup()
    return render_template('index.html', lookup = vlookup)

@app.before_request
def before_request():
    try:
        cart_data = session['cart']
        cart = SessionCart.from_storage(cart_data)
    except KeyError:
        cart = SessionCart()
    setattr(request, 'cart', cart)

@app.after_request
def after_request(request):
    if hasattr(request, 'cart') and request.cart.modified:
        request.cart.modified = False
        to_session = request.cart.for_storage()
        session['cart'] = to_session
    return request
