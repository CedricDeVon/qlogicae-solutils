__all__ = (
    "MacrosPluginManager",
)

_MacrosPluginManager = None
_ExternalDependencyManager = None

_MacrosDataManager = None


def _allocate():
    global _allocate
    global _MacrosPluginManager

    from .base_plugin_manager import BasePluginManager

    class __MacrosPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _MacrosDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _MacrosDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.macros_data_manager",
                            member="MacrosDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _MacrosDataManager
            })        

            return True


    _MacrosPluginManager = __MacrosPluginManager
    _allocate = lambda: None


def MacrosPluginManager():
    if _MacrosPluginManager is None:
        _allocate()

    return _MacrosPluginManager

