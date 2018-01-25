from functools import lru_cache
import contracts
from graph.dependency_graph import register_lazy_value_node


class LazyValueBase(object):
    def __init__(self):
        register_lazy_value_node(self)


@lru_cache(maxsize=None)
def get_lazy_value_type(value_type):
    """
    And, by the way, register it in contracts library
    """
    lazy_value_type = type(
        'LazyValue_{}'.format(value_type.__name__),
        (LazyValueBase,),
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
    globals()[lazy_value_type.__name__] = lazy_value_type
    contracts.new_contract(lazy_value_type.__name__, lazy_value_type)
    return lazy_value_type
