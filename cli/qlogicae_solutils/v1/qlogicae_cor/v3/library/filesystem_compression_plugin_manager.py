__all__ = (
    "FilesystemCompressionPluginManager",
)

_FilesystemCompressionPluginManager = None
_ExternalDependencyManager = None

_FilesystemCompressionDataManager = None


def _allocate():
    global _allocate
    global _FilesystemCompressionPluginManager

    from .base_plugin_manager import BasePluginManager

    class __FilesystemCompressionPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _FilesystemCompressionDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _FilesystemCompressionDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.filesystem_compression_data_manager",
                            member="FilesystemCompressionDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _FilesystemCompressionDataManager
            })        

            return True


    _FilesystemCompressionPluginManager = __FilesystemCompressionPluginManager
    _allocate = lambda: None


def FilesystemCompressionPluginManager():
    if _FilesystemCompressionPluginManager is None:
        _allocate()

    return _FilesystemCompressionPluginManager

