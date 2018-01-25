from abc import ABC, abstractmethod


class SerializerBase(ABC):
    @abstractmethod
    def serialize(self, memory_value):
        """
        returns in-memory serialized value
        """

    @abstractmethod
    def deserialize(self, serialized_value):
        """
        returns deserialized value
        """
