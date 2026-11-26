__all__ = (
    "ConsoleNavigationPluginManager",
)

_ConsoleNavigationPluginManager = None

_ConsoleNavigationDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _ConsoleNavigationPluginManager

    from .base_plugin_manager import BasePluginManager

    class __ConsoleNavigationPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager
            global _ConsoleNavigationDataManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _ConsoleNavigationDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.console_navigation_data_manager",
                            member="ConsoleNavigationDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _ConsoleNavigationDataManager
            })        

            return True


    _ConsoleNavigationPluginManager = __ConsoleNavigationPluginManager
    _allocate = lambda: None


def ConsoleNavigationPluginManager():
    if _ConsoleNavigationPluginManager is None:
        _allocate()

    return _ConsoleNavigationPluginManager


