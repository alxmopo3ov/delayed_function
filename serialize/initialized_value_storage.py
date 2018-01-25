from serialize.serialization_handler import SerializationHandler
from utils.singleton import SingletonBase


class InitializedValueStorage(SingletonBase):
    def __init__(self):
        self.__serialization_handler = SerializationHandler()
        self.__storage = {}

    def __delitem__(self, key):
        raise RuntimeError("Deleting items from ready storage is forbidden")

    def __getitem__(self, item):
        return self.__storage[item]

    def __len__(self):
        return len(self.__storage)

    def __setitem__(self, key, value):
        self.__storage[key] = self.__serialization_handler.serialize(value)


initialized_value_storage = InitializedValueStorage()
