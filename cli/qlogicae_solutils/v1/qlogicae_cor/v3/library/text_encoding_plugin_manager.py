__all__ = (
    "TextEncodingPluginManager",
)

_TextEncodingPluginManager = None
_ExternalDependencyManager = None

_TextEncodingDataManager = None


def _allocate():
    global _allocate
    global _TextEncodingPluginManager

    from .base_plugin_manager import BasePluginManager

    class __TextEncodingPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _TextEncodingDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _TextEncodingDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.text_encoding_data_manager",
                            member="TextEncodingDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _TextEncodingDataManager
            })        

            return True


    _TextEncodingPluginManager = __TextEncodingPluginManager
    _allocate = lambda: None


def TextEncodingPluginManager():
    if _TextEncodingPluginManager is None:
        _allocate()

    return _TextEncodingPluginManager

