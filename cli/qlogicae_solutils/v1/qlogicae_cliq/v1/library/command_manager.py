__all__ = (
    "CommandManager",
)

_CommandManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _CommandManager


    class __CommandManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError(
                    "'kwargs' must be a dictionary"
                )

            return True

        def shutdown(self):
            return True


    _CommandManager = __CommandManager
    _allocate = lambda: None


def CommandManager():
    if _CommandManager is None:
        _allocate()

    return _CommandManager



# CommandManager()
