__all__ = (
    "TextIoPluginManager",
)

_TextIoPluginManager = None
_ExternalDependencyManager = None

_TextIoDataManager = None


def _allocate():
    global _allocate
    global _TextIoPluginManager

    from .base_plugin_manager import BasePluginManager

    class __TextIoPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _TextIoDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _TextIoDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.text_io_data_manager",
                            member="TextIoDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _TextIoDataManager
            })        

            return True


    _TextIoPluginManager = __TextIoPluginManager
    _allocate = lambda: None


def TextIoPluginManager():
    if _TextIoPluginManager is None:
        _allocate()

    return _TextIoPluginManager

