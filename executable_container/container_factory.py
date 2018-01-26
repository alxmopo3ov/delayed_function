from executable_container.local_container import LocalContainer
from executable_container.nirvana_container import NirvanaContainer


container_types = ['nirvana', 'local']


def build_container(container_type, lazy_function):
    """
    :param container_type: type of container
    :param lazy_function: function wrapped with @lazy_function 
    :return: 
    """
    if container_type == 'nirvana':
        return NirvanaContainer(lazy_function)
    elif container_type == 'local':
        return LocalContainer(lazy_function)
    else:
        raise ValueError("Unknown container_type {}. it should be one of {}".format(container_type, container_types))
