from serialize import SerializationHandler
from serialize.default_serializer import DefaultSerializer
from types_lib.file_path import FilePath
import pytest


@pytest.yield_fixture()
def serialization_handler():
    yield SerializationHandler()


def function_generator():
    x = 105
    y = 106

    def f():
        return x, y

    return f


class SomeClass(object):
    def __init__(self):
        self.task = 105
        self.state = 106

    def __call__(self, *args, **kwargs):
        return self.task, self.state


class IntSerializer(object):
    def serialize(self, x):
        return str(x) + 'ahaha'

    def deserialize(self, x):
        return int(x[:-5])


@pytest.mark.parametrize('value', [1, 'parampam', function_generator(), SomeClass()], )
def test_serialization_with_only_default_serializer(serialization_handler, value):
    serialized = serialization_handler.serialize(value)
    deserialized = serialization_handler.deserialize(serialized, object)
    if not callable(value):
        assert deserialized == value
    else:
        assert deserialized() == (105, 106)


def test_replace_default_serializer(serialization_handler):
    with pytest.raises(KeyError):
        serialization_handler.add_serialization_hook(object, 'ahaha')
    with pytest.raises(KeyError):
        serialization_handler.add_serialization_hook(FilePath, 'ahaha')


def test_remove_default_serializer(serialization_handler):
    with pytest.raises(KeyError):
        serialization_handler.remove_serialization_hook(object)
    with pytest.raises(KeyError):
        serialization_handler.remove_serialization_hook(FilePath)


def test_custom_serialization_hook(serialization_handler):
    serialization_handler.add_serialization_hook(int, IntSerializer())
    res = serialization_handler.serialize(24)
    assert res == '24ahaha'
    assert type(serialization_handler.get_serializer(int)) == IntSerializer
    deserialized = serialization_handler.deserialize(res, int)
    assert deserialized == 24


def test_add_remove_custom_serialization_hook(serialization_handler):
    serialization_handler.add_serialization_hook(int, IntSerializer())
    assert type(serialization_handler.get_serializer(int)) == IntSerializer
    serialization_handler.remove_serialization_hook(int)
    assert type(serialization_handler.get_serializer(int)) == DefaultSerializer
