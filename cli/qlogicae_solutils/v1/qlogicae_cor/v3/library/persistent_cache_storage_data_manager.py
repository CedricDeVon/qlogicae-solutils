__all__ = (
    "PersistentCacheStoragePluginDataManager",
)

_ExternalDependencyManager = None
_PersistentCacheStoragePluginDataManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _PersistentCacheStoragePluginDataManager

    class __PersistentCacheStoragePluginDataManager:
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

        def setup(self, **kwargs):
            if not kwargs:
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
                    .setup_plugin_data(
                        root_key_path=self._root_key_path,
                        layer=0,
                        data=(
                            {
                                "root": (
                                    **self.write_setup_kwargs()
                                )
                            }
                        )
                    )
            )

        def read_root_data(self):
            plugin_data_manager = (
                _PluginDataManager()
                    .get_singleton()
            )

            return (
                plugin_data_manager
                    .read_one_data(
                        root_key_path=self._root_key_path,

                    )
            )

        def write_setup_kwargs(self, kwargs):
            if "database_path" not in kwargs:
                kwargs["database_path"] = "data.db"

            if "create_missing" not in kwargs:
                kwargs["create_missing"] = True

            if "lifespan_in_seconds" not in kwargs:
                kwargs["lifespan_in_seconds"] = 0.0

            if "file_mode" not in kwargs:
                kwargs["file_mode"] = 0o600

            if "key_encoding" not in kwargs:
                kwargs["key_encoding"] = "utf-8"

            if "auto_remove_expired" not in kwargs:
                kwargs["auto_remove_expired"] = True

            if "auto_remove_invalid" not in kwargs:
                kwargs["auto_remove_invalid"] = True

            if "sync_on_write" not in kwargs:
                kwargs["sync_on_write"] = False

            return kwargs


    _PersistentCacheStoragePluginDataManager = __PersistentCacheStoragePluginDataManager
    _allocate = lambda: None


def PersistentCacheStoragePluginDataManager():
    if _PersistentCacheStoragePluginDataManager is None:
        _allocate()

    return _PersistentCacheStoragePluginDataManager
