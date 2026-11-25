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

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
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
                    .setup_plugin_data({
                        "root_key_path": self._root_key_path,
                        "layer": 0,
                        "data": (
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
                    })
            )

        def read_company_name(self):
            return (
                self.read_one_data(
                    ("company_name"),
                ) or ""
            )

        def read_project_name(self):
            return (            
                self.read_one_data(
                    ("project_name"),
                ) or ""
            )

        def read_project_description(self):
            return (            
                self.read_one_data(
                    ("project_description"),
                ) or ""
            )

        def read_brand_base_name(self):
            return (            
                self.read_one_data(
                    ("brand_base_name"),
                ) or ""
            )

        def read_brand_source_name(self):
            return (            
                self.read_one_data(
                    ("brand_source_name"),
                ) or ""
            )

        def read_current_version_label(self):
            return (            
                self.read_one_data(
                    ("current_version_label"),
                ) or ""
            )

        def read_current_active_major_version_label(self):
            return (            
                self.read_one_data(
                    ("current_active_major_version_label"),
                ) or ""
            )

        def read_all_data(
            self
        ):
            data = (
                _PluginDataManager()
                    .get_singleton()
                    .read_all_data(
                        self._root_key_path
                    )
            )

            return (
                data
            )

        def read_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            data = (
                _PluginDataManager()
                    .get_singleton()
                    .read_one_data(
                        self._root_key_path,
                        key_path
                    )
            )

            return (
                data
            )

        def write_all_data(
            self,
            value
        ):
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .write_all_data(
                        self._root_key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def write_one_data(
            self,
            key_path,
            value,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .write_one_data(
                        self._root_key_path,
                        key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def remove_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .remove_one_data(
                        self._root_key_path,
                        key_path,
                    ) and result
            )

            return (
                result
            )

        def remove_all_data(
            self,
        ):
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .remove_all_data(
                        self._root_key_path,
                    ) and result
            )

            return (
                result
            )


    _BuildDataManager = __BuildDataManager
    _allocate = lambda: None


def BuildDataManager():
    if _BuildDataManager is None:
        _allocate()

    return _BuildDataManager
