import wtforms as forms


class AddToCartForm(forms.Form):

    quantity = forms.IntegerField(label='Quantity')
    submit = forms.SubmitField(label='Test')

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        self.product = kwargs.pop('product')
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def save(self):
        return self.cart.add(self.product, self.quantity.data or 1, check_quantity=True)

    def add_error(self, name, value):
        errors = self.errors.setdefault(name, value)
        errors.append(value)

class ReplaceCartLineForm(AddToCartForm):
    def __init__(self, *args, **kwargs):
        super(ReplaceCartLineForm, self).__init__(*args, **kwargs)
        self.cart_line = self.cart.get_line(self.product)

    def save(self):
        return self.cart.add(self.product, self.quantity, replace=True)
