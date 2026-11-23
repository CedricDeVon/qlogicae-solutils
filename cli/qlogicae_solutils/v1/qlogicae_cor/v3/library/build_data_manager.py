__all__ = (
    "BuildDataManager",
)

_BuildDataManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _BuildDataManager

    class __BuildDataManager:
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
        def key_path(self):
            return self._root_key_path

        @key_path.setter
        def key_path(self, value):
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
                "qlogicae_cor_v3_build"
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
                            {
                                "company_name": "",
                                "project_name": "",
                                "project_description": "",
                                "brand_base_name": "",
                                "brand_source_name": "",
                                "current_version_label": "",
                                "current_active_major_version_label": "",
                            }
                        )
                    )
            )


    _BuildDataManager = __BuildDataManager
    _allocate = lambda: None


def BuildDataManager():
    if _BuildDataManager is None:
        _allocate()

    return _BuildDataManager
