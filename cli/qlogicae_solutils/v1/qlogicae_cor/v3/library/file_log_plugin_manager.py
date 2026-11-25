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

    class __FileLogPluginManager:
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
            global _FileLogManager
            global _FileLogDataManager
        

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

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            file_log_data_manager = (
                _FileLogDataManager()
                    .read_singleton()
            )
            
            return (
                file_log_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):            
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

        def run_plugin(self):            
            result = True
            return result


        def shutdown_plugin(self):                        
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



