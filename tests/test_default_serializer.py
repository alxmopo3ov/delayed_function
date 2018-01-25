from serialize.default_serializer import DefaultSerializer
import pytest


@pytest.yield_fixture()
def serializer():
    yield DefaultSerializer()


def test_serialize_simple(serializer):
    dct = {
        1: 2,
        2: 'wefkbnfg',
        u'qcn': 2657,
        57: b'qfejowfveo'
    }
    res = serializer.serialize(dct)
    assert type(res) == str
    assert serializer.deserialize(res) == dct


# TODO: more conscious check
def test_serialize_objects(serializer):
    def function_generator(value):
        def func():
            return value
        return func

    obj = function_generator(346)
    res = serializer.serialize(obj)
    assert type(res) == bytes
    del obj, function_generator
    deserialized = serializer.deserialize(res)
    assert deserialized() == 346


def learn(task, state):
    return task, state


def test_serialize_simple_with_one_complex(serializer):
    dct = {
        1: 2,
        2: 'wefkbnfg',
        u'qcn': 2657,
        57: b'qfejowfveo',
        6: learn
    }

    res = serializer.serialize(dct)
    assert type(res) == bytes
    des = serializer.deserialize(res)
    # straight == comparison for functions is bad idea
    assert dct[6](1, 2) == des[6](1, 2)
    dct.pop(6)
    des.pop(6)
    assert des == dct


def test_improper_deserialization(serializer):
    with pytest.raises(TypeError):
        serializer.deserialize({1, 2, 3})
