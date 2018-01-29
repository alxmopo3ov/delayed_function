from serialize.serializer_base import SerializerBase
try:
    import ads.nirvana.automl.contrib_temp.cloudpickle as cloudpickle
except ImportError:
    import cloudpickle
import yaml
from yaml.representer import RepresenterError


class DefaultSerializer(SerializerBase):
    def serialize(self, memory_value):
        """
        If memory_value is "simple" type that can be safely serialized to yaml, then we will save it as 
        yaml in str instance
        Otherwise, we will serialize it by cloudpickle in bytes instance
        """
        try:
            return yaml.safe_dump(memory_value)
        except RepresenterError:
            return cloudpickle.dumps(memory_value)

    def deserialize(self, serialized_value):
        if isinstance(serialized_value, bytes):
            return cloudpickle.loads(serialized_value)
        elif isinstance(serialized_value, str):
            return yaml.safe_load(serialized_value)
        else:
            raise TypeError(
                "serialized_value should be either 'bytes' or 'str'; got\ntype {}\nvalue {}".format(
                    type(serialized_value),
                    serialized_value
                )
            )
