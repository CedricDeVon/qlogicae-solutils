__all__ = (
    "DebugManager",
)

_DebugManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _DebugManager

    from .abstract_manager import AbstractManager

    class __DebugManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

            return True


    _DebugManager = __DebugManager
    _allocate = lambda: None


def DebugManager():
    if _DebugManager is None:
        _allocate()

    return _DebugManager


# DebugManager()
