from lazy.lazy_value import LazyValueBase, get_lazy_value_type
from graph.dependency_graph import H
import pytest
import contracts


@pytest.yield_fixture()
def lazy_str():
    return get_lazy_value_type(str)


def test_lazy_value():
    v = LazyValueBase()
    assert v in H.dependency_graph
    assert v in H.dependency_graph.lazy_values


def test_get_lazy_value_has_value_type(lazy_str):
    assert lazy_str.value_type == str


def test_get_lazy_value_print(lazy_str):
    assert repr(lazy_str()) == "str"


def test_new_contracts_created():
    class Task(object):
        pass

    LazyTask = get_lazy_value_type(Task)

    @contracts.contract(task=Task, lazy_task=LazyTask)
    def learn(task, lazy_task):
        pass

    # if everything is ok, we should not obtain exception
    learn(Task(), LazyTask())

    with pytest.raises(contracts.ContractNotRespected):
        learn(1, LazyTask())

    with pytest.raises(contracts.ContractNotRespected):
        learn(Task(), "shshs")
