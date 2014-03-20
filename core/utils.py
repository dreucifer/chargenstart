""" @todo """
from flask import render_template, abort
from satchless.process import InvalidData, Step

class BaseStep(Step):
    """ @todo """
    forms = None
    template = ''
    group = None

    def __init__(self, request):
        """ @todo """
        self.request = request
        self.forms = dict()

    def __nonzero__(self):
        """ @todo """
        try:
            self.validate()
        except InvalidData:
            return False
        return True

    def save(self):
        """ @todo """
        raise NotImplementedError()

    def forms_are_valid(self):
        """ @todo """
        for form in self.forms.values():
            if not form.is_valid():
                return False
        return True

    def validate(self):
        """ @todo """
        if not self.forms_are_valid():
            raise InvalidData

    def process(self, extra_context=None):
        """ @todo """
        context = extra_context or dict()
        if not self.forms_are_valid() or self.request.method == 'GET':
            context['step'] = self
            return render_template(self.template, context = context)
        self.save()

    def get_absolute_url(self):
        """ @todo """
        raise NotImplementedError

def get_or_404(model, object_id):
    """ @todo """
    result = model.query.get(object_id)
    if result is None:
        abort(404)
    return result

def first_or_abort(model, **kwargs):
    """ @todo """
    result = model.query.filter_by(**kwargs).first()
    if result is None:
        abort(404)
    return result
