__all__ = (
    "FilesystemTemplateManager",
)

_FilesystemTemplateManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemTemplateManager

    from .abstract_manager import AbstractManager

    class __FilesystemTemplateManager(AbstractManager()):
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


    _FilesystemTemplateManager = __FilesystemTemplateManager
    _allocate = lambda: None


def FilesystemTemplateManager():
    if _FilesystemTemplateManager is None:
        _allocate()

    return _FilesystemTemplateManager


# FilesystemTemplateManager()
