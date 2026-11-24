__all__ = (
    "ConsoleLogPluginManager",
)

_ConsoleLogPluginManager = None
_ExternalDependencyManager = None

_LogOptions = None
_ConsoleLogManager = None
_PluginDataManager = None
_ConsoleLogDataManager = None


def _allocate():
    global _allocate
    global _ConsoleLogPluginManager

    class __ConsoleLogPluginManager:
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
            
            global _LogOptions
            global _ConsoleLogManager
            global _PluginDataManager
            global _ConsoleLogDataManager
        

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
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
            _LogOptions = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.log_options",
                        member="LogOptions",
                        is_member_callable=True,
                    )
            )
            _ConsoleLogManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.console_log_manager",
                        member="ConsoleLogManager",
                        is_member_callable=True,
                    )
            )
            _ConsoleLogDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.console_log_data_manager",
                        member="ConsoleLogDataManager",
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
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .get_singleton()
            )
            
            return (
                console_log_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):
            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .get_singleton()
            )
            
            plugin_data = (
                plugin_data_manager
                    .read_all_data(
                        console_log_data_manager
                            .root_key_path        
                    )
            )
            if not plugin_data:
                return True

            is_console_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )
            if is_console_logging_enabled_data:
                console_log_manager = (
                    _ConsoleLogManager()
                        .get_singleton()
                )

                result = (
                    console_log_manager
                        .setup(
                            options=_LogOptions()(
                                **plugin_data
                            )
                        ) and result
                )

            return result

        def run_plugin(self):            
            result = True
            return result


        def shutdown_plugin(self):            
            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .get_singleton()
            )
            
            plugin_data = (
                plugin_data_manager
                    .read_all_data(
                        console_log_data_manager
                            .root_key_path        
                    )
            )
            if not plugin_data:
                return True

            is_console_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )
            if is_console_logging_enabled_data:
                console_log_manager = (
                    _ConsoleLogManager()
                        .get_singleton()
                )

                result = (
                    console_log_manager
                        .shutdown() and result
                )

            return result


    _ConsoleLogPluginManager = __ConsoleLogPluginManager
    _allocate = lambda: None


def ConsoleLogPluginManager():
    if _ConsoleLogPluginManager is None:
        _allocate()

    return _ConsoleLogPluginManager
