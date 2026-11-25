__all__ = (
    "PersistentCacheStorageDataManager",
)

_ExternalDependencyManager = None
_PersistentCacheStorageDataManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _PersistentCacheStorageDataManager

    class __PersistentCacheStorageDataManager:
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

            global _PluginDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _PluginDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            self._root_key_path = (
                "qlogicae_cor_v3_persistent_cache_storage"
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def setup_plugin_data(self):
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
                                "root": {
                                    "database_path": "data.db",
                                    "create_missing": True,
                                    "lifespan_in_seconds": 0.0,
                                    "file_mode": 0o600,
                                    "key_encoding": "utf-8",
                                    "auto_remove_expired": True,
                                    "auto_remove_invalid": True,
                                    "sync_on_write": False,
                                }
                            }
                        )

                    })
            )

        def read_root_properties(self):
            return (
                self.read_one_data(
                    ("root",),
                )
            )

        def read_root_database_path(self):
            return (
                self.read_one_data(
                    ("root", "database_path",),
                )
            )

        def read_root_create_missing(self):
            return (
                self.read_one_data(
                    ("root", "create_missing",),
                )
            )

        def read_root_lifespan_in_seconds(self):
            return (
                self.read_one_data(
                    ("root", "lifespan_in_seconds",),
                )
            )

        def read_root_file_mode(self):
            return (
                self.read_one_data(
                    ("root", "file_mode",),
                )
            )

        def read_root_key_encoding(self):
            return (
                self.read_one_data(
                    ("root", "key_encoding",),
                )
            )

        def read_root_auto_remove_expired(self):
            return (
                self.read_one_data(
                    ("root", "auto_remove_expired",),
                )
            )

        def read_root_auto_remove_invalid(self):
            return (
                self.read_one_data(
                    ("root", "auto_remove_invalid",),
                )
            )

        def read_root_sync_on_write(self):
            return (
                self.read_one_data(
                    ("root", "sync_on_write",),
                )
            )

        def write_root_properties(self, value):
            return (
                self.write_one_data(
                    ("root",),
                    value
                )
            )

        def write_root_database_path(self, value):
            return (
                self.write_one_data(
                    ("root", "database_path",),
                    value
                )
            )

        def write_root_create_missing(self, value):
            return (
                self.write_one_data(
                    ("root", "create_missing",),
                    value
                )
            )

        def write_root_lifespan_in_seconds(self, value):
            return (
                self.write_one_data(
                    ("root", "lifespan_in_seconds",),
                    value
                )
            )

        def write_root_file_mode(self, value):
            return (
                self.write_one_data(
                    ("root", "file_mode",),
                    value
                )
            )

        def write_root_key_encoding(self, value):
            return (
                self.write_one_data(
                    ("root", "key_encoding",),
                    value
                )
            )

        def write_root_auto_remove_expired(self, value):
            return (
                self.write_one_data(
                    ("root", "auto_remove_expired",),
                    value
                )
            )

        def write_root_auto_remove_invalid(self, value):
            return (
                self.write_one_data(
                    ("root", "auto_remove_invalid",),
                    value
                )
            )

        def write_root_sync_on_write(self, value):
            return (
                self.write_one_data(
                    ("root", "sync_on_write",),
                    value
                )
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



    _PersistentCacheStorageDataManager = __PersistentCacheStorageDataManager
    _allocate = lambda: None


def PersistentCacheStorageDataManager():
    if _PersistentCacheStorageDataManager is None:
        _allocate()

    return _PersistentCacheStorageDataManager
