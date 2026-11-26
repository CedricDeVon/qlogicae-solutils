__all__ = (
    "ScriptProcessDelayManager",
)

_ScriptProcessDelayManager = None
_ExternalDependencyManager = None

_time = None


def _allocate():
    global _allocate
    global _ScriptProcessDelayManager

    from .abstract_manager import AbstractManager

    class __ScriptProcessDelayManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _time
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _time = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="time",
                    )
                )

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
