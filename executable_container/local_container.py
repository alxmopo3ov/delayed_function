from executable_container.container import ContainerBase


class LocalContainer(ContainerBase):
    def __init__(self, lazy_inputs_dct, lazy_function, lazy_outputs_dct, evaluated_dict):
        self.evaluated_dict = evaluated_dict
        self.lazy_inputs_dct = lazy_inputs_dct
        self.lazy_outputs_dct = lazy_outputs_dct
        super(LocalContainer, self).__init__(lazy_function)

    def load_inputs(self, local_data_storage):
        for input_name in self.inputs.keys():
            local_data_storage.inputs[input_name] = self.evaluated_dict[self.lazy_inputs_dct[input_name]]

    def save_outputs(self, local_data_storage):
        for output_id in range(len(self.outputs)):
            self.evaluated_dict[self.lazy_outputs_dct[output_id]] = local_data_storage.outputs[output_id]
