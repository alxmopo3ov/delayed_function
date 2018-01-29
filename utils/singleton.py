from utils.compatibility import lru_cache, with_metaclass


class Singleton(type):
    @lru_cache(maxsize=None)
    def __call__(cls, *args, **kwargs):
        new_cls = super(Singleton, cls).__call__(*args, **kwargs)
        return new_cls


class SingletonBase(with_metaclass(Singleton)):
    pass
