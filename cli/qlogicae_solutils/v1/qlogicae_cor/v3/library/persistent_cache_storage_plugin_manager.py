__all__ = (
    "PersistentCacheStoragePluginManager",
)

_ExternalDependencyManager = None
_PersistentCacheStoragePluginManager = None

_PersistentCacheStorageManager = None
_PersistentCacheStorageDataManager = None

def _allocate():
    global _allocate
    global _PersistentCacheStoragePluginManager

    class __PersistentCacheStoragePluginManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager
                    
            global _PersistentCacheStorageManager
            global _PersistentCacheStorageDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
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
            _PersistentCacheStorageDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.persistent_cache_storage_data_manager",
                        member="PersistentCacheStorageDataManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            persistent_cache_storage_data_manager = (
                _PersistentCacheStorageDataManager()
                    .get_singleton()
            )
            
            return (
                persistent_cache_storage_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):    
            result = True
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


    _PersistentCacheStoragePluginManager = __PersistentCacheStoragePluginManager
    _allocate = lambda: None


def PersistentCacheStoragePluginManager():
    if _PersistentCacheStoragePluginManager is None:
        _allocate()

    return _PersistentCacheStoragePluginManager

