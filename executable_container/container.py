from utils.abc_property_checker import ABCProp
from executable_container.local_data_storage import LocalDataStorage
from executable_container.function_executor import FunctionExecutor
from abc import abstractmethod


class ContainerBase(ABCProp):
    def __init__(self, delayed_function):
        """
        :param delayed_function: function wrapped with @delayed_function
        """
        self.inputs = delayed_function.inputs
        self.func = delayed_function.func
        self.outputs = delayed_function.outputs

    @abstractmethod
    def load_inputs(self, local_data_storage):
        """
        load inputs from some environment or database and fill local_data_storage with these data 
        """

    def run(self):
        """
        Run container. It will load inputs, execute function and save outputs
        """
        local_data_storage = LocalDataStorage()
        self.load_inputs(local_data_storage)
        executor = FunctionExecutor(self.inputs, self.func, self.outputs, local_data_storage, True)
        executor.run()
        self.save_outputs(local_data_storage)

    @abstractmethod
    def save_outputs(self, local_data_storage):
        """
        Send outputs from local_data_storage to environment or database
        """
