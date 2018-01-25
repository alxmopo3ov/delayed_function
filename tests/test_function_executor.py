from container.function_executor import FunctionExecutor, convert_return_value_to_tuple
from container.local_data_storage import LocalDataStorage
from serialize import SerializationHandler
import pytest


@pytest.yield_fixture()
def data_storage():
    return LocalDataStorage()


class Task(object):
    def __init__(self, x):
        self.x = x + 10

    def __eq__(self, other):
        return self.x == other.x


def test_read_inputs(data_storage):
    handler = SerializationHandler()
    data_storage.inputs.update(
        {
            'x': handler.serialize(24),
            'y': handler.serialize('607'),
            'z': handler.serialize(Task(2))
        }
    )
    inputs = dict(x=int, y=str, z=Task)
    cnt = FunctionExecutor(inputs, None, None, data_storage, type_check=True)
    assert cnt.get_inputs() == {
        'x': 24,
        'y': '607',
        'z': Task(2)
    }


def test_write_outputs(data_storage):
    serializer = SerializationHandler()
    cnt = FunctionExecutor(None, None, (int, str, Task, float), data_storage, type_check=True)
    cnt.save_outputs((1, 'ahaha', Task(3), 3.4))
    assert data_storage.outputs == {
        0: serializer.serialize(1),
        1: serializer.serialize('ahaha'),
        2: serializer.serialize(Task(3)),
        3: serializer.serialize(3.4)
    }


def test_type_check_violated(data_storage):
    cnt = FunctionExecutor(None, None, (int, str, Task, int), data_storage, type_check=True)
    with pytest.raises(TypeError):
        cnt.save_outputs((1, 'ahaha', Task(3), 3.4))


def test_convert_value_to_tuple():
    def f():
        pass

    def g():
        return 1

    def k():
        return 1, 2, 3

    assert convert_return_value_to_tuple(f()) == ()
    assert convert_return_value_to_tuple(g()) == (1, )
    assert convert_return_value_to_tuple(k()) == (1, 2, 3)


def test_run(data_storage):
    handler = SerializationHandler()
    data_storage.inputs.update(
        {
            'x': handler.serialize(24),
            'y': handler.serialize('607'),
            'z': handler.serialize(Task(2))
        }
    )
    inputs = dict(x=int, y=str, z=Task)
    outputs = (int, str, Task, float)

    def f(x, y, z):
        return x, y, z, float(z.x) * 2.3

    cnt = FunctionExecutor(inputs, f, outputs, data_storage, type_check=True)
    cnt.run()

    assert data_storage.outputs == {
        0: handler.serialize(24),
        1: handler.serialize('607'),
        2: handler.serialize(Task(2)),
        3: handler.serialize(12 * 2.3)
    }


def test_run_with_no_return(data_storage):
    handler = SerializationHandler()
    data_storage.inputs.update(
        {
            'x': handler.serialize(24),
            'y': handler.serialize('607'),
            'z': handler.serialize(Task(2))
        }
    )
    inputs = dict(x=int, y=str, z=Task)
    outputs = ()

    def f(x, y, z):
        print(x, y, z)

    cnt = FunctionExecutor(inputs, f, outputs, data_storage, type_check=True)
    cnt.run()
    assert data_storage.outputs == {}


def test_inconsistent_empty_output(data_storage):
    cnt = FunctionExecutor(None, None, (int, ), data_storage)
    with pytest.raises(RuntimeError):
        cnt.check_output_consistency(None)


def test_consistent_empty_output(data_storage):
    cnt = FunctionExecutor(None, None, (), data_storage)
    cnt.check_output_consistency(None)


def test_inconsistent_nonempty_output(data_storage):
    cnt = FunctionExecutor(None, None, (int, ), data_storage)
    with pytest.raises(RuntimeError):
        cnt.check_output_consistency((2, 4))
