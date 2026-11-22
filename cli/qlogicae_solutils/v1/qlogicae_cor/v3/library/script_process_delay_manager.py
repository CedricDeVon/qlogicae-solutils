__all__ = (
    "ScriptProcessDelayManager",
)

_time = None
_ScriptProcessDelayManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _ScriptProcessDelayManager

    class __ScriptProcessDelayManager:
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
            global _time
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _time = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="time",
                )
            )

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def delay_process(
            self,
            value,
        ):
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError("")

            _time = (
                _time()
            )

            _time.sleep(value)

            return True


    _ScriptProcessDelayManager = __ScriptProcessDelayManager
    _allocate = lambda: None


def ScriptProcessDelayManager():
    if _ScriptProcessDelayManager is None:
        _allocate()

    return _ScriptProcessDelayManager


# ScriptProcessDelayManager()
