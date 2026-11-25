__all__ = (
    "FilesystemDataManager",
)

_ExternalDependencyManager = None
_FilesystemDataManager = None

_os = None
_pathlib = None
_PluginDataManager = None


def _allocate():
    global _allocate
    global _FilesystemDataManager

    class __FilesystemDataManager:
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
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _os
            global _pathlib

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _os = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(
                        path="os",
                    )
            )
            _pathlib = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(
                        path="pathlib",
                    )
            )

            self._root_key_path = (
                "qlogicae_cor_v3_filesystem"
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
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            plugin_data_manager = (
                _PluginDataManager()
                    .read_singleton()
            )

            return (
                plugin_data_manager
                    .setup_plugin_data({
                        "root_key_path": self._root_key_path,
                        "layer": 0,
                        "data": {
                            "default_remove_excluded_filesystem_paths": (
                                _pathlib().Path(_os().path.abspath(_os().fspath(
                                    _pathlib().Path.cwd()
                                ))),
                            ),
                            "callbacks": {
                                "on_pre_setup": None,
                                "on_post_setup": None,
                                "on_pre_run": None,
                                "on_post_run": None,
                                "on_pre_shutdown": None,
                                "on_post_shutdown": None,
                            },
                        }
                    })
            )

        def read_default_remove_excluded_filesystem_paths(self):
            return (
                self.read_one_data(
                    ("default_remove_excluded_filesystem_paths",),
                )
            )

        def read_all_data(
            self
        ):
            data = (
                _PluginDataManager()
                    .read_singleton()
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
                    .read_singleton()
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
                    .read_singleton()
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
                    .read_singleton()
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
                    .read_singleton()
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
                    .read_singleton()
                    .remove_all_data(
                        self._root_key_path,
                    ) and result
            )

            return (
                result
            )


    _FilesystemDataManager = __FilesystemDataManager
    _allocate = lambda: None


def FilesystemDataManager():
    if _FilesystemDataManager is None:
        _allocate()

    return _FilesystemDataManager
