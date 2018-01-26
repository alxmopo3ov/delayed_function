from collections import MutableMapping


class InitializedValueStorage(MutableMapping):
    __storage = {}

    def __delitem__(self, key):
        del self.__storage[key]

    def __getitem__(self, item):
        return self.__storage[item]

    def __iter__(self):
        return iter(self.__storage)

    def __len__(self):
        return len(self.__storage)

    def __setitem__(self, key, value):
        self.__storage[key] = value


initialized_value_storage = InitializedValueStorage()
