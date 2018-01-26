from lazy.lazy_utils import validate_function, convert_to_python_return, check_all_are_types
import pytest


def test_check_all_types():
    check_all_are_types(None, (int, float))
    with pytest.raises(TypeError):
        check_all_are_types(None, (int, 23.4))


def test_convert_to_python_return():
    assert convert_to_python_return(()) is None
    assert convert_to_python_return((1, )) == 1
    assert convert_to_python_return((2, 3, 4)) == (2, 3, 4)


def test_validate_function():
    def proper(x, y, z = 1):
        pass
    validate_function(proper)


def test_validate_bad_function():
    def imp1(x, y, *args):
        pass

    def imp2(x, y, **kwargs):
        pass

    def imp3(x, y, *args, **kwargs):
        pass

    with pytest.raises(TypeError):
        validate_function(imp1)
    with pytest.raises(TypeError):
        validate_function(imp2)
    with pytest.raises(TypeError):
        validate_function(imp3)
