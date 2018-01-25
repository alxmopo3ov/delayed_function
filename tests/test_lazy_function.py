from lazy.lazy_function import lazy_function, convert_to_lazy_value, LazyValueBase
from serialize.initialized_value_storage import initialized_value_storage
from serialize.serialization_handler import SerializationHandler
import pytest


def test_convert_to_lazy():
    value = u'156'
    h = SerializationHandler()
    lazy_value = convert_to_lazy_value(value)
    assert initialized_value_storage[lazy_value] == h.serialize(value)
    assert isinstance(lazy_value, LazyValueBase)
