from utils.singleton import SingletonBase


def test__singleton_without_args():
    class A(SingletonBase):
        pass

    a, b, c = A(), A(), A()

    assert a is b
    assert b is c


def test__singleton_with_args():
    class B(SingletonBase):

        def __init__(self, *args, **kwargs):
            self.args = args
            for k, v in kwargs.items():
                setattr(self, k, v)

    a, b, c = B(1, 2, meta=3), B(1, 2, meta=3), B(1, 2, meta=3)
    assert a is b
    assert b is c
    d = B(1, 2, meta=4)
    assert c is not d
