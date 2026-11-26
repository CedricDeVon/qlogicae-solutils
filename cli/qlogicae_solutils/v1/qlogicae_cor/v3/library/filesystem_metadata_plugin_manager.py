__all__ = (
    "FilesystemMetadataPluginManager",
)

_FilesystemMetadataPluginManager = None
_ExternalDependencyManager = None

_FilesystemMetadataDataManager = None


def _allocate():
    global _allocate
    global _FilesystemMetadataPluginManager

    from .base_plugin_manager import BasePluginManager

    class __FilesystemMetadataPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _FilesystemMetadataDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _FilesystemMetadataDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.filesystem_metadata_data_manager",
                            member="FilesystemMetadataDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _FilesystemMetadataDataManager
            })        

            return True


    _FilesystemMetadataPluginManager = __FilesystemMetadataPluginManager
    _allocate = lambda: None


def FilesystemMetadataPluginManager():
    if _FilesystemMetadataPluginManager is None:
        _allocate()

    return _FilesystemMetadataPluginManager

