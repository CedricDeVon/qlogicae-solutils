__all__ = (
    "BuildPluginManager",
)

_BuildPluginManager = None

_BuildDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _BuildPluginManager

    from .base_plugin_manager import BasePluginManager

    class __BuildPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager   
            global _BuildDataManager

            if not _ExternalDependencyManager:                
                from .external_dependency_manager import ExternalDependencyManager    

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _BuildDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.build_data_manager",
                            member="BuildDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _BuildDataManager
            })        

            return True


    _BuildPluginManager = __BuildPluginManager
    _allocate = lambda: None


def BuildPluginManager():
    if _BuildPluginManager is None:
        _allocate()

    return _BuildPluginManager


