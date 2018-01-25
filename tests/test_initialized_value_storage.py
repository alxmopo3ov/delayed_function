from serialize.initialized_value_storage import initialized_value_storage
from serialize.serialization_handler import SerializationHandler
import pytest


def test_add_value():
    key = 1
    value = '100500'
    initialized_value_storage[key] = value
    assert initialized_value_storage[key] == SerializationHandler().serialize(value)
    assert len(initialized_value_storage) == 1


def test_remove_value():
    key = 1
    value = '100500'
    initialized_value_storage[key] = value
    with pytest.raises(RuntimeError):
        del initialized_value_storage[key]
