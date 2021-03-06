from runner.local_runner import run_local
from delayed.delayed_function import delayed_function, build_dependency_graph
import pytest
from numbers import Number


@pytest.yield_fixture()
def simple_graph():
    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def add(x, y):
        return x + 1, y + 1

    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def mul(x, y):
        return x * 10, y * 10

    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def div(x, y):
        return x / 2, y / 2

    @delayed_function(outputs=[Number] * 4, inputs=dict(x=Number, y=Number, z=Number, w=Number))
    def print_nums(x, y, z, w):
        return x, y, z, w

    with build_dependency_graph("some_test_graph"):
        a, b = add(1, 2)
        c, d = mul(3, 4)
        e, f = div(b, c)
        delayed_res = print_nums(*(mul(a, e) + add(f, d)))

    a, b = add(1, 2)
    c, d = mul(3, 4)
    e, f = div(b, c)
    reference = print_nums(*(mul(a, e) + add(f, d)))

    yield delayed_res, reference


# TODO: when i will be able to build graphs with multiple inputs, i must create test for it


def test_graph(simple_graph):
    delayed_res, reference = simple_graph
    delayed_values = run_local("some_test_graph")
    for i in range(len(reference)):
        assert delayed_values[delayed_res[i]] == reference[i]
