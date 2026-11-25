__all__ = (
    "ScriptProcessPluginManager",
)

_ExternalDependencyManager = None
_ScriptProcessPluginManager = None

_ScriptProcessDataManager = None


def _allocate():
    global _allocate
    global _ScriptProcessPluginManager

    class __ScriptProcessPluginManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            
            global _ScriptProcessDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _ScriptProcessDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.script_process_data_manager",
                        member="ScriptProcessDataManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            script_process_data_manager = (
                _ScriptProcessDataManager()
                    .get_singleton()
            )
            
            return (
                script_process_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):
            result = True
            return result

        def run_plugin(self):            
            result = True
            return result

        def shutdown_plugin(self):            
            result = True
            return result


    _ScriptProcessPluginManager = __ScriptProcessPluginManager
    _allocate = lambda: None


def ScriptProcessPluginManager():
    if _ScriptProcessPluginManager is None:
        _allocate()

    return _ScriptProcessPluginManager


