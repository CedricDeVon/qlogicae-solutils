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

    from .base_plugin_manager import BasePluginManager

    class __ConsoleLogPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager
            global _ConsoleLogDataManager
            
            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _LogOptions
                global _ConsoleLogManager
            
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

            self.base_construct({
                "data_manager": _ConsoleLogDataManager
            })        

            return True

        def setup_plugin_hook(self):            
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

        def run_plugin_hook(self):            
            result = True
            return result


        def shutdown_plugin_hook(self):                        
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
