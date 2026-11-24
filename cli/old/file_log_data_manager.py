__all__ = (
    "FileLogPluginDataManager",
)

_FileLogPluginDataManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _FileLogPluginDataManager

    class __FileLogPluginDataManager:
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

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            self._key_path = (
                "qlogicae_cor_v3_file_log"
            )

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def setup_plugin_data(self):
            global _PluginDataManager
            
            _PluginDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )

            return (
                plugin_data_manager
                    .setup_plugin_data(
                        key_path=self._key_path,
                        layer=0,
                        data=(
                            {
                                "is_enabled": False,
                                "is_verbose_enabled": True,
                                "log_level": 10,
                                "stack_level": 3,
                                "target_filesystem_paths": [],
                            }
                        )
                    )
            )


    _FileLogPluginDataManager = __FileLogPluginDataManager
    _allocate = lambda: None


def FileLogPluginDataManager():
    if _FileLogPluginDataManager is None:
        _allocate()

    return _FileLogPluginDataManager
