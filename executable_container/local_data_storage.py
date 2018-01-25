class LocalDataStorage(object):
    def __init__(self):
        self.__inputs = {}
        self.__outputs = {}

    def clear(self):
        self.__inputs = {}
        self.__outputs = {}

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs
