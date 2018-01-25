import os
from utils.singleton import SingletonBase


class Environment(SingletonBase):
    def __init__(self):
        self.container_type = os.environ['LAZY_FUNCTION_CONTAINER_TYPE']
