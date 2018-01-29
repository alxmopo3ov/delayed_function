try:
    from functools import lru_cache
except ImportError:
    from ads.nirvana.automl.contrib_temp.repoze import lru_cache


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    if not bases:
        bases = (object, )
    return meta("NewBase", bases, {})
