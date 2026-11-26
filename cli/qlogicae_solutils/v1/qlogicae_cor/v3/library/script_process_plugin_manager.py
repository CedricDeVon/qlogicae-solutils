__all__ = (
    "ScriptProcessPluginManager",
)

_ExternalDependencyManager = None
_ScriptProcessPluginManager = None

_ScriptProcessDataManager = None


def _allocate():
    global _allocate
    global _ScriptProcessPluginManager

    from .base_plugin_manager import BasePluginManager

    class __ScriptProcessPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _ScriptProcessDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _ScriptProcessDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.script_process_data_manager",
                            member="ScriptProcessDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _ScriptProcessDataManager
            })        

            return True


    _ScriptProcessPluginManager = __ScriptProcessPluginManager
    _allocate = lambda: None


def ScriptProcessPluginManager():
    if _ScriptProcessPluginManager is None:
        _allocate()

    return _ScriptProcessPluginManager


