__all__ = (
    "JsonIoPluginManager",
)

_ExternalDependencyManager = None
_JsonIoPluginManager = None

_JsonIoDataManager = None


def _allocate():
    global _allocate
    global _JsonIoPluginManager

    from .base_plugin_manager import BasePluginManager

    class __JsonIoPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _JsonIoDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _JsonIoDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.json_io_data_manager",
                            member="JsonIoDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _JsonIoDataManager
            })        

            return True


    _JsonIoPluginManager = __JsonIoPluginManager
    _allocate = lambda: None


def JsonIoPluginManager():
    if _JsonIoPluginManager is None:
        _allocate()

    return _JsonIoPluginManager

