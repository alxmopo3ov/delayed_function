from serialize.initialized_value_storage import initialized_value_storage
import pytest


@pytest.yield_fixture()
def storage():
    initialized_value_storage.clear()
    yield initialized_value_storage
    initialized_value_storage.clear()


def test_add_value(storage):
    key = 1
    value = '100500'
    storage[key] = value
    assert storage[key] == value
    assert len(storage) == 1
