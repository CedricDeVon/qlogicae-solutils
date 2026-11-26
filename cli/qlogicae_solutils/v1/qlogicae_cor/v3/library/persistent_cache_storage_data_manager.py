__all__ = (
    "PersistentCacheStorageDataManager",
)

_ExternalDependencyManager = None
_PersistentCacheStorageDataManager = None


def _allocate():
    global _allocate
    global _PersistentCacheStorageDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __PersistentCacheStorageDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "persistent_cache_storage"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
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
                    }                  
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


    _PersistentCacheStorageDataManager = __PersistentCacheStorageDataManager
    _allocate = lambda: None


def PersistentCacheStorageDataManager():
    if _PersistentCacheStorageDataManager is None:
        _allocate()

    return _PersistentCacheStorageDataManager
