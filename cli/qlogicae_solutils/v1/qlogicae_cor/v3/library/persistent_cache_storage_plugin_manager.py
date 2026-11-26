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

    from .base_plugin_manager import BasePluginManager

    class __PersistentCacheStoragePluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _PersistentCacheStorageManager
                global _PersistentCacheStorageDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _PersistentCacheStorageManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.persistent_cache_storage_manager",
                            member="PersistentCacheStorageManager",
                            is_member_callable=True,
                        )
                )
                _PersistentCacheStorageDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.persistent_cache_storage_data_manager",
                            member="PersistentCacheStorageDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _PersistentCacheStorageDataManager
            })        

            return True

        def on_run_plugin(self):
            persistent_cache_storage_manager = (
                _PersistentCacheStorageManager()
                    .read_singleton()
            )

            result = True
            result = (
                persistent_cache_storage_manager.open() and result
            )

            return result

        def on_shutdown_plugin(self):
            persistent_cache_storage_manager = (
                _PersistentCacheStorageManager()
                    .read_singleton()
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

