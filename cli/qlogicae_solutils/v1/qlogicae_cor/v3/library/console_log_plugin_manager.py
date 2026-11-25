__all__ = (
    "ConsoleLogPluginManager",
)

_ConsoleLogPluginManager = None
_ExternalDependencyManager = None

_LogOptions = None
_ConsoleLogManager = None
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
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            
            global _LogOptions
            global _ConsoleLogManager
            global _ConsoleLogDataManager
        

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _LogOptions = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.log_options",
                        member="LogOptions",
                        is_member_callable=True,
                    )
            )
            _ConsoleLogManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.console_log_manager",
                        member="ConsoleLogManager",
                        is_member_callable=True,
                    )
            )
            _ConsoleLogDataManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.console_log_data_manager",
                        member="ConsoleLogDataManager",
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
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .read_singleton()
            )
            
            return (
                console_log_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):            
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .read_singleton()
            )
            
            plugin_data = (
                console_log_data_manager
                    .read_all_data()
            )
            if not plugin_data:
                return True

            is_console_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )

            result = True
            if is_console_logging_enabled_data:
                console_log_manager = (
                    _ConsoleLogManager()
                        .read_singleton()
                )

                result = (
                    console_log_manager
                        .setup({
                            "options": _LogOptions()(
                                **plugin_data
                            )
                        }) and result
                )

            return result

        def run_plugin(self):            
            result = True
            return result


        def shutdown_plugin(self):                        
            console_log_data_manager = (
                _ConsoleLogDataManager()
                    .read_singleton()
            )
            
            plugin_data = (
                console_log_data_manager
                    .read_all_data()
            )
            if not plugin_data:
                return True

            is_console_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )

            result = True
            if is_console_logging_enabled_data:
                console_log_manager = (
                    _ConsoleLogManager()
                        .read_singleton()
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
