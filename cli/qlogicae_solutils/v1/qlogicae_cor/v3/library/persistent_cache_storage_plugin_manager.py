__all__ = (
    "PluginManager",
)

_ExternalDependencyManager = None
_PersistentCacheStoragePluginManager = None

_PluginManager = None
_PersistentCacheStorageManager = None

def _allocate():
    global _allocate
    global _PersistentCacheStoragePluginManager

    class __PersistentCacheStoragePluginManager:
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
            global _PersistentCacheStorageManager

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
            _PersistentCacheStorageManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.persistent_cache_storage_manager",
                        member="PersistentCacheStorageManager",
                        is_member_callable=True,
                    )
            )

            self._key_path = (
                "qlogicae",
                "cor",
                "v3",
                "persistent_cache_storage",
            )
            
            return True

        def setup(self, **kwargs):
            if not kwargs
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
                            "root": {
                                "database_path": "data.db",
                                "create_missing": True,
                                "lifespan_in_seconds": 0.0,
                                "file_mode": 0o600,
                                "key_encoding": "utf-8",
                                "auto_remove_expired": True,
                                "auto_remove_invalid": True,
                                "sync_on_write": False,
                            },
                        },
                    )
            )

            return initial_data

        def setup_plugin(self):
            plugin_data = (
                self.read_data() or {}
            )
            if not plugin_data:
                return True
                
            persistent_cache_storage_manager = (
                _PersistentCacheStorageManager()
                    .get_singleton()
            )
            root_data = (
                plugin_data.get(
                    "root",
                    {}
                ) or {}
            )

            result = True
            result = (
                persistent_cache_storage_manager
                    .setup(
                        **root_data
                    ) and result
            )

            return result

        def run_plugin(self):
            persistent_cache_storage_manager = (
                _PersistentCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                persistent_cache_storage_manager.open() and result
            )

            return result

        def shutdown_plugin(self):
            persistent_cache_storage_manager = (
                _PersistentCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                persistent_cache_storage_manager.close() and result
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


    _PersistentCacheStoragePluginManager = __PersistentCacheStoragePluginManager
    _allocate = lambda: None


def PersistentCacheStoragePluginManager():
    if _PersistentCacheStoragePluginManager is None:
        _allocate()

    return _PersistentCacheStoragePluginManager

