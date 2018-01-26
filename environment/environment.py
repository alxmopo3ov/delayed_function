import os


class Environment(object):
    @property
    def function_name(self):
        return os.environ['DELAYED_FUNCTION_FUNCTION_NAME']
