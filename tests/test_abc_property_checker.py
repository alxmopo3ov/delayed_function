from utils.abc_property_checker import ABCProp
import abc
import pytest


@pytest.yield_fixture()
def Base():
    class MyBaseClass(ABCProp):

        @abc.abstractproperty
        def f(self):
            return 1

    yield MyBaseClass


def test_direct_inheritance(Base):
    class Derived(Base):
        @property
        def f(self):
            return 2

    assert Derived().f == 2


def test_direct_improper_inheritance(Base):
    with pytest.raises(AttributeError):
        class Derived(Base):
            def f(self):
                return 2


def test_indirect_inheritance(Base):
    class Derived1(Base):
        @property
        def f(self):
            return 2

    class Derived2(Base):
        @property
        def f(self):
            return 3

    assert Derived2().f == 3


def test_indirect_improper_inheritance(Base):
    class Derived1(Base):
        @property
        def f(self):
            return 2

    with pytest.raises(AttributeError):
        class Derived2(Base):
            def f(self):
                return 3


def test_indirect_inheritance2(Base):
    class Derived1(Base):
        pass

    class Derived2(Base):
        @property
        def f(self):
            return 3

    assert Derived2().f == 3


def test_indirect_improper_inheritance2(Base):
    class Derived1(Base):
        pass

    with pytest.raises(AttributeError):
        class Derived2(Base):
            def f(self):
                return 3
