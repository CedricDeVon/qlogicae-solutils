__all__ = (
    "SystemPluginManager",
)

_SystemPluginManager = None
_ExternalDependencyManager = None

_SystemManager = None
_PluginDataManager = None
_SystemDataManager = None


def _allocate():
    global _allocate
    global _SystemPluginManager

    class __SystemPluginManager:
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

            global _SystemManager
            global _PluginDataManager
            global _SystemDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _SystemManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.system_manager",
                        member="SystemManager",
                        is_member_callable=True,
                    )
            )
            _PluginDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )
            _SystemDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.system_data_manager",
                        member="SystemDataManager",
                        is_member_callable=True,
                    )
            )
            
            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            system_data_manager = (
                _SystemDataManager()
                    .get_singleton()
            )
            
            return (
                system_data_manager
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


    _SystemPluginManager = __SystemPluginManager
    _allocate = lambda: None


def SystemPluginManager():
    if _SystemPluginManager is None:
        _allocate()

    return _SystemPluginManager

