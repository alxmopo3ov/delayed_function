from functools import lru_cache


class Singleton(type):
    @lru_cache(maxsize=None)
    def __call__(cls, *args, **kwargs):
        new_cls = super(Singleton, cls).__call__(*args, **kwargs)
        return new_cls


class SingletonBase(metaclass=Singleton):
    pass
