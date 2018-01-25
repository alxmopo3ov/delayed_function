from utils.mro import get_nearest_class


def test_direct_inheritance():
    class A(object):
        pass

    class B(A):
        pass

    assert get_nearest_class(B, {B, A, object}) == B
    assert get_nearest_class(B, {A, object}) == A
    assert get_nearest_class(B, {object}) == object
    assert get_nearest_class(B, {}) == object


def test_nested_direct_inheritance():
    class A(object):
        pass

    class B(A):
        pass

    class C(B):
        pass

    assert get_nearest_class(C, {B, A}) == B


def test_simple_multiple_inheritance():
    class A(object):
        pass

    class B(object):
        pass

    class C(A, B):
        pass

    assert get_nearest_class(C, {A, B}) == A
    assert get_nearest_class(C, {B}) == B
