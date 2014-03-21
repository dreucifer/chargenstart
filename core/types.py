from sqlalchemy.types import TypeDecorator, UserDefinedType, CHAR, Float
import uuid
from numbers import Number
from prices import Price

class GUID(TypeDecorator):
    """ Platform independent GUID type.

    Uses uses CHAR(32), storing as str'ified
    hex values.

    """

    impl = CHAR

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return "%.32x" % value
        elif value and not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value)
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(value)
        else:
            return None

class PriceField(TypeDecorator):
    """ Price field mapping prices module object to database field """

    impl = Float

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, Price):
            if value.currency != self.currency:
                raise ValueError('Invalid Currency: %r (expected %r)' % (
                    value.currency, self.currency))
            return value.net
        if value and isinstance(value, Number):
            return value
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return Price(value, currency=self.currency)
        else:
            return None
