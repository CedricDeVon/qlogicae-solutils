__all__ = (
    "AbstractManager",
)

_AbstractManager = None

def _allocate():
    global _allocate
    global _AbstractManager

    class __AbstractManager:
        __slots__ = ()

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        def construct(self):
            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True
                
            return True

        def shutdown(self):
            return True

        @classmethod
        def read_singleton(cls):
            if cls.__dict__.get("_singleton") is None:
                cls._singleton = cls()

            return cls._singleton


    _AbstractManager = __AbstractManager
    _allocate = lambda: None


def AbstractManager():
    if _AbstractManager is None:
        _allocate()

    return _AbstractManager


# AbstractManager()

