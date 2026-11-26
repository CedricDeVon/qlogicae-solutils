__all__ = (
    "FilesystemPluginManager",
)

_FilesystemPluginManager = None
_ExternalDependencyManager = None

_FilesystemDataManager = None


def _allocate():
    global _allocate
    global _FilesystemPluginManager

    from .base_plugin_manager import BasePluginManager

    class __FilesystemPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _FilesystemDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _FilesystemDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.filesystem_data_manager",
                            member="FilesystemDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _FilesystemDataManager
            })        

            return True


    _FilesystemPluginManager = __FilesystemPluginManager
    _allocate = lambda: None


def FilesystemPluginManager():
    if _FilesystemPluginManager is None:
        _allocate()

    return _FilesystemPluginManager

