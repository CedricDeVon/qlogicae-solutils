__all__ = (
    "TimePluginManager",
)

_TimePluginManager = None
_ExternalDependencyManager = None

_TimeZoneManager = None
_PluginDataManager = None
_TimeDataManager = None


def _allocate():
    global _allocate
    global _TimePluginManager

    class __TimePluginManager:
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

            global _TimeZoneManager
            global _PluginDataManager
            global _TimeDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _TimeZoneManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.time_zone_manager",
                        member="TimeZoneManager",
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
            _TimeDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.time_data_manager",
                        member="TimeDataManager",
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
            time_data_manager = (
                _TimeDataManager()
                    .get_singleton()
            )
            
            return (
                time_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):
            time_data_manager = (
                _TimeDataManager()
                    .get_singleton()
            )
            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )
            plugin_data = (
                plugin_data_manager
                    .read_all_data(
                        time_data_manager
                            .root_key_path        
                    )
            )
            if not plugin_data:
                return True

            time_zone_manager = (
                _TimeZoneManager()
                    .get_singleton()
            )
            result = True
            result = (
                time_zone_manager
                    .setup(
                        **plugin_data
                    ) and result
            )

            return result

        def run_plugin(self):            
            result = True
            return result


        def shutdown_plugin(self):            
            result = True
            return result


    _TimePluginManager = __TimePluginManager
    _allocate = lambda: None


def TimePluginManager():
    if _TimePluginManager is None:
        _allocate()

    return _TimePluginManager

