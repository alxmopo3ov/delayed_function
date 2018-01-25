import os
from utils.singleton import SingletonBase


class Environment(SingletonBase):
    def __init__(self):
        self.container_type = os.environ['LAZY_FUNCTION_CONTAINER_TYPE']
        self.function_name = os.environ['LAZY_FUNCTION_FUNCTION_NAME']
