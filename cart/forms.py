import wtforms as forms


class QuantityField(forms.IntegerField):

    def __init__(self, *args, **kwargs):
        super(QuantityField, self).__init__(min_value=0,
                                            max_value=999,
                                            initial=1)


class AddToCartForm(forms.Form):

    quantity = QuantityField(label='Quantity')
    error_messages = {
        'empty-stock': 'Sorry, this product is currently out of stock',
        'variant-does-not-exist': 'Oops. We could not find that product',
        'insufficient-stock': 'Only %(remaining)d remaining in stock.'
    }

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        self.product = kwargs.pop('product')
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def save(self):
        return self.cart.add(self.product, self.quantity)

    def add_error(self, name, value):
        errors = self.errors.setdefault(name, value)
        errors.append(value)
