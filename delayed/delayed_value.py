from functools import lru_cache
import contracts
from graph.dependency_graph import register_delayed_value_node
from serialize.initialized_value_storage import initialized_value_storage


class DelayedValueBase(object):
    def __init__(self):
        register_delayed_value_node(self)


@lru_cache(maxsize=None)
def get_delayed_value_type(value_type):
    """
    And, by the way, register it in contracts library
    """
    delayed_value_type = type(
        'DelayedValue_{}'.format(value_type.__name__),
        (DelayedValueBase,),
        {
            'value_type': value_type,
            '__repr__': lambda self: self.value_type.__name__
        }
    )
    try:
        contracts.new_contract(value_type.__name__, value_type)
    except ValueError:
        # value is a built-in or it has already been registered in pycontracts
        pass
    # register created type as global name
    globals()[delayed_value_type.__name__] = delayed_value_type
    contracts.new_contract(delayed_value_type.__name__, delayed_value_type)
    return delayed_value_type


def convert_to_delayed_value(value):
    delayed_value = get_delayed_value_type(type(value))()
    initialized_value_storage[delayed_value] = value
    return delayed_value
