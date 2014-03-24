""" @todo """
from flask import render_template, request, flash
from product import Products
from product.models import Product
from cart.forms import AddToCartForm
from cart import ShoppingCart
from core.utils import get_or_404, first_or_abort

@Products.route('/', methods=['POST', 'GET'])
def index():
    """ @todo """
    products = Product.query.all()
    cart = ShoppingCart.for_session_cart(request.cart)
    forms = [AddToCartForm(product=product, cart=cart) for product in products]

    for form in forms:
        if form.validate():
            flash('product added to cart')
            form.save()
    return render_template('products.html', products=products, forms=forms, cart=cart)

@Products.route('/info/<product_id>', methods=['GET', 'POST'])
def details(product_id):
    """ @todo """
    product = get_or_404(Product, product_id)
    cart = ShoppingCart.for_session_cart(request.cart)
    form = AddToCartForm()


    if form.validate():
        flash('product added to cart')
    return render_template('details.html', product=product, form=form)
