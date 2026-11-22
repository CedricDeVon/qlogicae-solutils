__all__ = (
    "FileLogPluginManager",
)

_FileLogPluginManager = None
_ExternalDependencyManager = None

_LogOptions = None
_FileLogManager = None
_PluginManager = None


def _allocate():
    global _allocate
    global _FileLogPluginManager

    class __FileLogPluginManager:
        __slots__ = (
            "_key_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def key_path(self):
            return self._key_path

        @key_path.setter
        def key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._key_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
            global _PluginManager
            global _LogOptions
            global _FileLogManager
        

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _PluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_manager",
                        member="PluginManager",
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
            _FileLogManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.file_log_manager",
                        member="FileLogManager",
                        is_member_callable=True,
                    )
            )

            self._key_path = (
                "qlogicae",
                "cor",
                "v3",
                "file_log"
            )
            
            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            moduli_plugin_manager = (
                _PluginManager()
                    .get_singleton()
            )
            
            initial_data = (
                moduli_plugin_manager
                    .setup_data(
                        moduli={ "layer": 0 },
                        key_path=self._key_path,
                        data={
                            "is_enabled": False,
                            "is_verbose_enabled": True,
                            "log_level": 10,
                            "stack_level": 3,
                            "target_filesystem_paths": [],
                        },
                    )
            )

            return initial_data

        def setup_plugin(self):
            result = True
            plugin_data = (
                self.read_data() or {}
            )
            if not plugin_data:
                return True

            file_data = (
                plugin_data.get(
                    "file",
                    {}
                ) or {}
            )
            is_file_logging_enabled_data = (
                file_data.get(
                    "is_enabled",
                    False
                )
            )
            if is_file_logging_enabled_data:
                file_log_manager = (
                    _FileLogManager()
                        .get_singleton()
                )
                result = (
                    file_log_manager
                        .setup(
                            options=_LogOptions()(
                                **file_data
                            )
                        ) and result
                )

            return result

        def run_plugin(self):
            return True

        def shutdown_plugin(self):
            result = True
            plugin_data = (
                self.read_data() or {}
            )
            if not plugin_data:
                return True

            file_data = (
                plugin_data.get(
                    "file",
                    {}
                ) or {}
            )
            is_file_logging_enabled_data = (
                file_data.get(
                    "is_enabled",
                    False
                )
            )
            if is_file_logging_enabled_data:
                file_log_manager = (
                    _FileLogManager()
                        .get_singleton()
                )
                result = (
                    file_log_manager
                        .shutdown() and result
                )

            return result

        def read_data(self):
            moduli_plugin_manager = (
                _PluginManager()
                    .get_singleton()
            )

            return (
                moduli_plugin_manager
                    .read_data(
                        keys=self._key_path,
                    )
            )


    _FileLogPluginManager = __FileLogPluginManager
    _allocate = lambda: None


def FileLogPluginManager():
    if _FileLogPluginManager is None:
        _allocate()

    return _FileLogPluginManager

