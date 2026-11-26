__all__ = (
    "HttpManager",
)

_HttpManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _HttpManager

    from .abstract_manager import AbstractManager

    class __HttpManager(AbstractManager()):
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


    _HttpManager = __HttpManager
    _allocate = lambda: None


def HttpManager():
    if _HttpManager is None:
        _allocate()

    return _HttpManager


# HttpManager()
