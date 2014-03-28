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

from math import ceil

class Pagination(object):

    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        assert self.query is not None, \
                'a query object is required for this to work'
        return get_for_page(self.query, self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self, error_out=False):
        assert self.query is not None, \
                'a query object is required for this to work'
        return get_for_page(self.query, self.page + 1, self.per_page, error_out)

    @property
    def next_num(self):
        return self.page + 1
    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
            right_edge=2, right_current=5):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

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

def get_for_page(query, page=1, per_page=20, error_out=True):
    if error_out and page < 1:
        abort(404)
    offset = (page - 1) * per_page
    items = query.limit(per_page).offset(offset).all()
    if not items and page != 1 and error_out:
        abort(404)
    if page == 1  and len(items) < per_page:
        total = len(items)
    else:
        total = query.count()

    return Pagination(query, page, per_page, total, items)
