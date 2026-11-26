__all__ = (
    "FileLogPluginManager",
)

_FileLogPluginManager = None
_ExternalDependencyManager = None

_LogOptions = None
_FileLogManager = None
_FileLogDataManager = None


def _allocate():
    global _allocate
    global _FileLogPluginManager

    from .base_plugin_manager import BasePluginManager

    class __FileLogPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager
                    
            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _LogOptions
                global _FileLogManager
                global _FileLogDataManager

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
                _FileLogManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.file_log_manager",
                            member="FileLogManager",
                            is_member_callable=True,
                        )
                )
                _FileLogDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.file_log_data_manager",
                            member="FileLogDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _FileLogDataManager
            })        

            return True

        def setup_plugin_hook(self):            
            file_log_data_manager = (
                _FileLogDataManager()
                    .read_singleton()
            )
            
            plugin_data = (
                file_log_data_manager
                    .read_all_data()
            )
            if not plugin_data:
                return True

            is_file_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )

            result = True
            if is_file_logging_enabled_data:
                file_log_manager = (
                    _FileLogManager()
                        .read_singleton()
                )

                result = (
                    file_log_manager
                        .setup({
                            "options": _LogOptions()(
                                **plugin_data
                            )
                        }) and result
                )

            return result

        def shutdown_plugin_hook(self):                        
            file_log_data_manager = (
                _FileLogDataManager()
                    .read_singleton()
            )
            
            plugin_data = (
                file_log_data_manager
                    .read_all_data()
            )
            if not plugin_data:
                return True

            is_file_logging_enabled_data = (
                plugin_data.get(
                    "is_enabled",
                    False
                )
            )

            result = True
            if is_file_logging_enabled_data:
                file_log_manager = (
                    _FileLogManager()
                        .read_singleton()
                )

                result = (
                    file_log_manager
                        .shutdown() and result
                )

            return result


    _FileLogPluginManager = __FileLogPluginManager
    _allocate = lambda: None


def FileLogPluginManager():
    if _FileLogPluginManager is None:
        _allocate()

    return _FileLogPluginManager



