from utils.abc_property_checker import ABCProp
from abc import abstractmethod


class ExecutableContainerBase(ABCProp):
    def run(self):
        """
        Run container. It will load inputs, execute function and save outputs
        """