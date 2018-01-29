from executable_container.container import ContainerBase
from delayed.delayed_value import DelayedDictBase, DelayedListBase


class LocalContainer(ContainerBase):
    def __init__(self, delayed_inputs_dct, delayed_function, delayed_outputs_dct, serialized_evaluated_dict):
        self.serialized_evaluated_dict = serialized_evaluated_dict
        self.delayed_inputs_dct = delayed_inputs_dct
        self.delayed_outputs_dct = delayed_outputs_dct
        super(LocalContainer, self).__init__(delayed_function)

    def load_inputs(self, local_data_storage):
        for input_name in self.inputs.keys():
            if issubclass(self.inputs[input_name], DelayedListBase):
                cur_value = [self.serialized_evaluated_dict[self.delayed_inputs_dct[input_name][x]]
                             for x in sorted(self.delayed_inputs_dct[input_name].keys())]
            elif issubclass(self.inputs[input_name], DelayedDictBase):
                cur_value = {x: self.serialized_evaluated_dict[self.delayed_inputs_dct[input_name][x]]
                             for x in self.delayed_inputs_dct[input_name].keys()}
            else:
                cur_value = self.serialized_evaluated_dict[self.delayed_inputs_dct[input_name]]
            local_data_storage.inputs[input_name] = cur_value

    def save_outputs(self, local_data_storage):
        for output_id in range(len(self.outputs)):
            self.serialized_evaluated_dict[self.delayed_outputs_dct[output_id]] = local_data_storage.outputs[output_id]
