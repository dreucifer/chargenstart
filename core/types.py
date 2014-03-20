from sqlalchemy.types import TypeDecorator, CHAR, Float
import uuid
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
            return value.net
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return Price(value)
        else:
            return None
