import pytest
from contracts import ContractException
from utils.type_check import do_type_check


@pytest.yield_fixture()
def no_args_func():
    def func():
        pass

    yield func


@pytest.yield_fixture()
def no_default_args_func():
    def learn(task, state):
        pass

    yield learn


@pytest.yield_fixture()
def args_and_kwargs_func():
    def train(task, state, pool='alxmopo3ov'):
        pass

    yield train


def test_type_check_no_args(no_args_func):
    do_type_check(no_args_func, (), {}, {})


def test_type_check_no_args_wrong(no_args_func):
    with pytest.raises(ContractException):
        do_type_check(no_args_func, (), {}, {'task': int})


def test_type_check_no_default(no_default_args_func):
    do_type_check(no_default_args_func, (1, 2), {}, {'task': int, 'state': int})


def test_type_check_no_default_pass_as_kw(no_default_args_func):
    do_type_check(no_default_args_func, (1,),
                  {'state': 2}, {'task': int, 'state': int})


def test_type_check_no_default_wrong(no_default_args_func):
    with pytest.raises(ContractException):
        do_type_check(no_default_args_func, (1, 2), {},
                      {'task': int, 'state': float})


def test_type_check_all_positional(args_and_kwargs_func):
    do_type_check(args_and_kwargs_func, (1, 2, 'alxmopo3ov'), {},
                  {'task': int, 'state': int, 'pool': str})


def test_type_check_do_not_set_default(args_and_kwargs_func):
    do_type_check(args_and_kwargs_func, (1, 2), {},
                  {'task': int, 'state': int, 'pool': str})


def test_type_check_all_kw(args_and_kwargs_func):
    do_type_check(args_and_kwargs_func, (),
                  {'task': 1, 'state': 2, 'pool': 'alxmopo3ov'},
                  {'task': int, 'state': int, 'pool': str})


def test_type_check_all_kw_without_default(args_and_kwargs_func):
    do_type_check(args_and_kwargs_func, (),
                  {'task': 1, 'state': 2},
                  {'task': int, 'state': int, 'pool': str})


def test_type_check_all_kw_wrong_default_type(args_and_kwargs_func):
    with pytest.raises(ContractException):
        do_type_check(args_and_kwargs_func, (),
                      {'task': 1, 'state': 2},
                      {'task': int, 'state': int, 'pool': int})
