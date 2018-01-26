import os


class Environment(object):
    @property
    def container_type(self):
        return os.environ['DELAYED_FUNCTION_CONTAINER_TYPE']

    @property
    def function_name(self):
        return os.environ['DELAYED_FUNCTION_FUNCTION_NAME']
