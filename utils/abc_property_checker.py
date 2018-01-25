import abc
import itertools
from pprint import pformat


class ABCPropertyCheckMeta(abc.ABCMeta):
    """
    This class just checks that abc.abstractproperty are instantiated using @property decorator
    """
    def __new__(cls, name, bases, attr_dict):
        # construct new type with patched attributes dictionary
        cls = super(ABCPropertyCheckMeta, cls).__new__(cls, name, bases, attr_dict)

        # collect all abstract properties
        base_abstractproperties = set().union(
            itertools.chain.from_iterable(getattr(b, '__abstractproperties__', set()) for b in bases)
        )

        for key, value in attr_dict.items():
            if isinstance(value, abc.abstractproperty):
                base_abstractproperties.add(key)

        cls.__abstractproperties__ = frozenset(base_abstractproperties)

        # check that all abstract properties are indeed properties
        improperly_overriden_properties = []
        for key, value in attr_dict.items():
            if key in cls.__abstractproperties__ and not isinstance(value, property):
                improperly_overriden_properties.append(key)

        if improperly_overriden_properties:
            raise AttributeError("Missing @property decorator for instantiation of \n{}\n abstract properties".format(
                pformat(improperly_overriden_properties)))

        return cls


class ABCProp(metaclass=ABCPropertyCheckMeta):
    pass
