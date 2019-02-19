import uuid
from datetime import datetime, timezone

from schematizer.exceptions import SimpleValidationError
from schematizer.schemas.base import BaseCoercibleSchema, BaseSchema


class Dummy(BaseSchema):
    def to_native(self, obj):
        return obj

    def to_primitive(self, obj):
        return obj


class Bool(BaseCoercibleSchema):
    TRUE_VALUES = (True, 1, '1', 'true', 't', 'yes', 'y', 'on')
    FALSE_VALUES = (False, 0, '0', 'false', 'f', 'no', 'n', 'off')

    coerce_native = bool

    def to_native(self, obj):
        if obj in self.TRUE_VALUES:
            return True
        if obj in self.FALSE_VALUES:
            return False
        else:
            raise SimpleValidationError('UNMARSHABLE', extra={
                'message': f'not a boolean: {obj!r}',
            })


class Int(BaseCoercibleSchema):
    coerce_primitive = int
    coerce_native = int


class Float(BaseCoercibleSchema):
    coerce_primitive = float
    coerce_native = float


class Str(BaseCoercibleSchema):
    coerce_primitive = str
    coerce_native = str


class UUID(BaseCoercibleSchema):
    coerce_primitive = uuid.UUID
    coerce_native = str


class Enum(BaseCoercibleSchema):
    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type

    def coerce_primitive(self, obj):
        return self.enum_type(obj)

    def coerce_native(self, obj):
        return self.enum_type(obj).value


class DateTime(BaseCoercibleSchema):
    def coerce_primitive(self, obj):
        return datetime.utcfromtimestamp(float(obj))

    def coerce_native(self, obj):
        return obj.replace(tzinfo=timezone.utc).timestamp()