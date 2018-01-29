from utils.compatibility import lru_cache
import contracts
from graph.dependency_graph import register_delayed_value_node
from serialize.initialized_value_storage import initialized_value_storage


class DelayedValueBase(object):
    def __init__(self):
        register_delayed_value_node(self)


class DelayedCollectionBase(object):
    value_type = None

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.value_type.__name__)


class DelayedListBase(DelayedCollectionBase):
    pass


class DelayedDictBase(DelayedCollectionBase):
    pass


@lru_cache(maxsize=None)
def DelayedList(value_type):
    return type(
        'DelayedList_{}'.format(value_type.__name__),
        (DelayedListBase, ),
        {'value_type': value_type}
    )


@lru_cache(maxsize=None)
def DelayedDict(value_type):
    return type(
        'DelayedDict_{}'.format(value_type.__name__),
        (DelayedDictBase,),
        {'value_type': value_type}
    )


def generate_delayed_inputs(values, inputs):
    """
    :param values: values that were passed to function call 
    :param inputs: dict(input_name=input_type)
    :return: 
    """
    res = {}
    for key, value in values.items():
        if issubclass(inputs[key], DelayedListBase):
            res[key] = {
                'seq_item_{}'.format(i): convert_to_delayed_if_necessary(input_value)
                for i, input_value in enumerate(value)
            }
        elif issubclass(inputs[key], DelayedDictBase):
            res[key] = {
                input_key: convert_to_delayed_if_necessary(input_value)
                for input_key, input_value in value.items()
            }
        else:
            res[key] = convert_to_delayed_if_necessary(value)
    return res


def convert_to_delayed_if_necessary(value):
    if isinstance(value, DelayedValueBase):
        return value
    else:
        return convert_to_delayed_value(value)


def generate_delayed_outputs(output_types):
    if output_types:
        return tuple(get_delayed_value_type(x)() for x in output_types)
    else:
        return ()


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
