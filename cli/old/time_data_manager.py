__all__ = (
    "TimeDataManager",
)

_TimeDataManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _TimeDataManager

    class __TimeDataManager:
        __slots__ = (
            "_root_key_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def root_key_path(self):
            return self._root_key_path

        @root_key_path.setter
        def root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._root_key_path = value

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

            self._root_key_path = (
                "qlogicae_cor_v3_time"
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
                        root_key_path=self._root_key_path,
                        layer=0,
                        data=(
                            self.write_setup_kwargs({})
                        )
                    )
            )

        def write_setup_kwargs(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            if "selected_time_zone_type" not in kwargs:
                kwargs["selected_time_zone_type"] = "local"

            if "valid_time_zone_types" not in kwargs:
                kwargs["valid_time_zone_types"] = { "local", "utc" }

            return kwargs


    _TimeDataManager = __TimeDataManager
    _allocate = lambda: None


def TimeDataManager():
    if _TimeDataManager is None:
        _allocate()

    return _TimeDataManager
