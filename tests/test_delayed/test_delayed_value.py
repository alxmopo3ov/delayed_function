from delayed.delayed_value import DelayedValueBase, get_delayed_value_type, convert_to_delayed_value
from serialize.initialized_value_storage import initialized_value_storage
from graph.dependency_graph import H
import pytest
import contracts


@pytest.yield_fixture()
def storage():
    initialized_value_storage.clear()
    yield initialized_value_storage
    initialized_value_storage.clear()


@pytest.yield_fixture()
def delayed_str():
    return get_delayed_value_type(str)


def test_delayed_value():
    v = DelayedValueBase()
    assert v in H.dependency_graph
    assert v in H.dependency_graph.delayed_values


def test_get_delayed_value_has_value_type(delayed_str):
    assert delayed_str.value_type == str


def test_get_delayed_value_print(delayed_str):
    assert repr(delayed_str()) == "str"


def test_new_contracts_created():
    class Task(object):
        pass

    DelayedTask = get_delayed_value_type(Task)

    @contracts.contract(task=Task, delayed_task=DelayedTask)
    def learn(task, delayed_task):
        pass

    # if everything is ok, we should not obtain exception
    learn(Task(), DelayedTask())

    with pytest.raises(contracts.ContractNotRespected):
        learn(1, DelayedTask())

    with pytest.raises(contracts.ContractNotRespected):
        learn(Task(), "shshs")


def test_convert_to_delayed(storage):
    value = u'156'
    delayed_value = convert_to_delayed_value(value)
    assert storage[delayed_value] == value
    assert isinstance(delayed_value, DelayedValueBase)
