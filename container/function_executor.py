from serialize import SerializationHandler


def convert_return_value_to_tuple(outputs):
    if outputs is None:
        return ()
    elif not isinstance(outputs, tuple):
        return outputs,
    else:
        return outputs


def check_output_type(value, value_type, output_id):
    if not isinstance(value, value_type):
        raise TypeError(
            "Violated type checking. output_id = {} must be instance of {}, but got {}".format(
                output_id,
                value_type,
                type(value).__name__
            )
        )


class FunctionExecutor(object):
    def __init__(self, container_inputs, func, container_outputs, local_data_storage, type_check=False):
        """
        Get inputs from local_data_storage, calculate func(**inputs) and send outputs to local_data_storage
        :param container_inputs: dict(input_name=input_type)
        :param func: callable func.
        :param container_outputs: (type, type, type)
        :param type_check: 
        """
        self.container_inputs = container_inputs
        self.func = func
        self.container_outputs = container_outputs
        self.serialization_handler = SerializationHandler()
        self.local_data_storage = local_data_storage
        self.type_check = type_check

    def get_inputs(self):
        res = {}
        for name, value_type in self.container_inputs.items():
            serialized = self.get_serialized_input(name)
            res[name] = self.serialization_handler.deserialize(serialized, value_type)
        return res

    def run(self):
        calculated_inputs = self.get_inputs()
        calculated_outputs = self.func(**calculated_inputs)
        calculated_outputs = convert_return_value_to_tuple(calculated_outputs)
        self.check_output_consistency(calculated_outputs)
        self.save_outputs(calculated_outputs)

    def save_outputs(self, calculated_outputs):
        for calced_out, (output_id, expected_value_type) in zip(calculated_outputs, enumerate(self.container_outputs)):
            if self.type_check:
                check_output_type(calced_out, expected_value_type, output_id)
            serialized = self.serialization_handler.serialize(calced_out)
            self.send_serialized_output(serialized, output_id)

    def get_serialized_input(self, input_name):
        """
        Read serialized value of input with input_name from storage
        """
        return self.local_data_storage.inputs[input_name]

    def send_serialized_output(self, serialized_output, output_id):
        """
        Read serialized output with some id to storage
        """
        self.local_data_storage.outputs[output_id] = serialized_output

    def check_output_consistency(self, calculated_outputs):
        if calculated_outputs is None:
            if len(self.container_outputs):
                raise RuntimeError(
                    "Inconsistent number of output values. "
                    "Function did not return anything or returned None; "
                    "container_outputs must be tuple(), got {}".format(self.container_outputs)
                )
        elif len(calculated_outputs) != len(self.container_outputs):
            raise RuntimeError(
                "Inconsistent number of return values. "
                "Function returned {} values, but it must return "
                "len(self.container_outputs) = {} values".format(len(calculated_outputs), len(self.container_outputs))
            )
