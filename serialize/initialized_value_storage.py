from utils.singleton import SingletonBase


class InitializedValueStorage(SingletonBase, dict):
    pass


initialized_value_storage = InitializedValueStorage()
