""" @todo: Docstring """
from flask import Blueprint, request, session
from satchless import cart as scart
from prices import Price
from product.models import Product

Cart = Blueprint('cart', __name__, url_prefix='/cart',
                 template_folder='cart/templates',
                 static_folder='cart/static')

import cart.admin


class ShoppingCart(scart.Cart):
    timestamp = None
    billing_address = None

    def __init__(self, session_cart):
        super(ShoppingCart, self).__init__()
        self.session_cart = session_cart

    @classmethod
    def for_session_cart(cls, session_cart):
        shoppingcart = ShoppingCart(session_cart)
        product_ids = [item.data['product_id'] for item in session_cart]
        products = Product.query.filter(Product.id_ in product_ids).all()
        product_map = dict((p.id_, p) for p in products)
        for item in session_cart:
            try:
                product = product_map[item.data['product_id']]
            except KeyError:
                continue
            quantity = item.quantity
            shoppingcart.add(product, quantity=quantity, check_quantity=False)
        return shoppingcart

    def __str__(self):
        return "Shopping Cart, Your Cart({0})".format(self.count())

    def get_data_for_product(self, product):
        product_price = product.get_price_per_item()
        product_data = {
                'product_id': product.id_,
                'unit_price_gross': str(product_price.gross),
                'unit_price_net': str(product_price.net)}
        return product_data

    def add(self, product, quantity=1, data=None, replace=False,
            check_quantity=True):
        super(ShoppingCart, self).add(product, quantity, data,
                                      replace, check_quantity)
        data = self.get_data_for_product(product)
        self.session_cart.add(str(product), quantity, data,
                              replace=True)

    def clear(self):
        super(ShoppingCart, self).clear()
        self.session_cart.clear()


class SessionCartLine(scart.CartLine):

    def get_price_per_item(self, **kwargs):
        gross = self.data['unit_price_gross']
        net = self.data['unit_price_net']
        return Price(gross=gross, net=net)

    @property
    def serialize(self):
        return {
            'product': self.product,
            'quantity': self.quantity,
            'data': self.data}

    @classmethod
    def from_storage(cls, data_dict):
        product = data_dict.pop('product')
        quantity = data_dict.pop('quantity')
        data = data_dict['data']
        instance = SessionCartLine(product, quantity, data=data)
        return instance


class SessionCart(scart.Cart):

    def __str__(self):
        return 'SessionCart'

    @classmethod
    def from_storage(cls, cart_data):
        cart = SessionCart()
        for line_data in cart_data['items']:
            cart._state.append(SessionCartLine.from_storage(line_data))
        return cart

    @property
    def serialize(self):
        cart_data = {
            'items': [i.serialize for i in self]}
        return cart_data

    def create_line(self, product, quantity, data):
        return SessionCartLine(product, quantity, data)

@Cart.before_app_request
def before_app_request():
    try:
        cart_data = session['cart']
        cart = SessionCart.from_storage(cart_data)
    except KeyError:
        cart = SessionCart()
    setattr(request, 'cart', cart)
    setattr(request, 'test', 'test')

@Cart.after_app_request
def after_app_request(request):
    if hasattr(request, 'cart'):
        to_session = request.cart.serialize
        session['cart'] = to_session
    return request
