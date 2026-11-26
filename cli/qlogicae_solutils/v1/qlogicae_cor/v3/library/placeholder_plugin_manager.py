__all__ = (
    "PlaceholderPluginManager",
)

_PlaceholderPluginManager = None
_ExternalDependencyManager = None

_PlaceholderDataManager = None


def _allocate():
    global _allocate
    global _PlaceholderPluginManager

    from .base_plugin_manager import BasePluginManager

    class __PlaceholderPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _PlaceholderDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _PlaceholderDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.placeholder_data_manager",
                            member="PlaceholderDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _PlaceholderDataManager
            })        

            return True


    _PlaceholderPluginManager = __PlaceholderPluginManager
    _allocate = lambda: None


def PlaceholderPluginManager():
    if _PlaceholderPluginManager is None:
        _allocate()

    return _PlaceholderPluginManager


