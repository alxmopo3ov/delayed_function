from utils.mro import get_nearest_class
from serialize.default_serializer import DefaultSerializer
from types_lib.file_path import FilePath, FilePathSerializer


class SerializationHandler(object):
    """
    This class just implements interfaces for data serialization-deserialization. Generally, almost everything
    can be serialized-deserialized via cloudpickle library, but this is very inconvenient when launching in
    some cloud environment: you will not be able to see simple outputs like dicts or strings in the interface
    """
    serialization_hooks = {
        object: DefaultSerializer(),
        FilePath: FilePathSerializer()
    }

    def add_serialization_hook(self, serialization_type, serializer):
        if serialization_type in {object, FilePath}:
            raise KeyError("Cannot replace default serializer for {}".format(serialization_type))
        self.serialization_hooks[serialization_type] = serializer

    def remove_serialization_hook(self, serialization_type):
        if serialization_type in {object, FilePath}:
            raise KeyError("Cannot remove default serializer for {}".format(serialization_type))
        self.serialization_hooks.pop(serialization_type)

    def get_serializer(self, value_type):
        if value_type in self.serialization_hooks:
            # simple case: exact match by type
            return self.serialization_hooks[value_type]
        else:
            # more complicated case: let's define the nearest serializer
            nearest_cls = get_nearest_class(value_type, set(self.serialization_hooks.keys()))
            return self.serialization_hooks[nearest_cls]

    def serialize(self, memory_value):
        return self.get_serializer(type(memory_value)).serialize(memory_value)

    def deserialize(self, serialized_value, serialized_value_type):
        return self.get_serializer(serialized_value_type).deserialize(serialized_value)
