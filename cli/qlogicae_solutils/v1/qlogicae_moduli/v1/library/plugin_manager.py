__all__ = (
    "PluginManager",
)

_PluginManager = None
_ObjectMergeManager = None
_PythonModuleManager = None
_ValueCacheStorageManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
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
            global _ValueCacheStorageManager
            global _PythonModuleManager
            global _ObjectMergeManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _ObjectMergeManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(
                        path="qlogicae_cor.v3.library.object_merge_manager",
                        member="ObjectMergeManager",
                        is_member_callable=True,
                    )
            )
            _PythonModuleManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(
                        path="qlogicae_cor.v3.library.python_module_manager",
                        member="PythonModuleManager",
                        is_member_callable=True,
                    )
            )
            _ValueCacheStorageManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(
                        path="qlogicae_cor.v3.library.value_cache_storage_manager",
                        member="ValueCacheStorageManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(
            self,
            **kwargs,
        ):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            plugin_exports = (
                self.read_plugin_exports(
                    **kwargs
                )
            )
            plugin_export_data_collection = (
                self.read_plugin_export_data(
                    plugin_exports
                )
            )

            self.setup_value_cache_storage_database(
                kwargs,
                plugin_export_data_collection
            )

            return True

        def shutdown(self):
            return True

        def read_plugin_export_data(
            self,
        ):
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            return (
                value_cache_storage_manager.read_all_items()
            )

        def read_plugin_exports(
            self,
            **kwargs,
        ):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            target_filesystem_paths = (
                kwargs.get("target_filesystem_paths", tuple()) or tuple()
            )
            is_recursive = (
                kwargs.get("is_recursive", True)
            )
            internal_objects = (
                kwargs.get("internal_objects", tuple()) or tuple()
            )
            internal_modules = (
                kwargs.get("internal_modules", tuple()) or tuple()
            )
            external_objects = (
                kwargs.get("external_objects", tuple()) or tuple()
            )

            external_modules = tuple()        
            if target_filesystem_paths:
                external_modules = tuple(
                    _PythonModuleManager()
                        .get_singleton()
                        .read_imported_modules(
                            target_filesystem_paths,
                            is_recursive
                        )
                )

            outputs = (
                internal_objects +
                internal_modules +
                external_objects +
                external_modules
            )

            return (
                outputs
            )

        def read_plugin_export_data(
            self,
            plugin_exports
        ):
            if not isinstance(plugin_exports, (tuple, list)) or not plugin_exports:
                raise ValueError("'plugin_exports' must either be a non-empty tuple or list")

            plugin_export_data_collection = [
                self.read_plugin_export(
                    plugin_export
                ) for plugin_export in plugin_exports
            ]

            plugin_export_data_collection.sort(
                key=lambda item: (item.get('merge_layer', 0) or 0)
            )

            return tuple(
                plugin_export_data_collection
            )

        def setup_value_cache_storage_database(
            self,
            kwargs,
            plugin_export_data_collection
        ):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            if not isinstance(plugin_export_data_collection, (tuple, list)) or not plugin_export_data_collection:
                raise ValueError("'plugin_export_data_collection' must either be a non-empty tuple or list")

            object_merge_manager = (
                _ObjectMergeManager().get_singleton()
            )
            value_cache_storage_manager = (
                _ValueCacheStorageManager().get_singleton()
            )
            
            internal_export_data = (
                kwargs.get("internal_export_data", tuple()) or tuple()
            )
            initial_export_data = (
                kwargs.get("initial_export_data", {}) or {}
            )

            plugin_export_data_collection = (
                tuple(plugin_export_data_collection) + internal_export_data
            )

            module_exports = (
                object_merge_manager.deep_merge(
                    self.read_plugin_export_data(),
                    initial_export_data
                )
            )
            for plugin_export_data in plugin_export_data_collection:
                if not isinstance(plugin_export_data, (dict)):
                    raise ValueError("'plugin_export_data' must be a dictionary")

                module_exports = (
                    object_merge_manager.deep_merge(
                        module_exports,
                        plugin_export_data
                    )
                )

            if not module_exports:
                value_cache_storage_manager.set_all_items(
                    values=module_exports
                )

            return True

        def read_plugin_export(
            self,
            plugin_export,
        ):
            if not plugin_export:
                raise ValueError("'plugin_export' must be defined")

            plugin_export_data = (
                plugin_export.export()
            )

            return (
                plugin_export_data
            )

        def setup_data(
            self,
            **kwargs
        ):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            keys = (
                kwargs.get(
                    "keys",
                    ()
                ) or ()
            )
            merge_layer = (
                kwargs.get(
                    "merge_layer",
                    0
                ) or 0
            )
            data = (
                kwargs.get(
                    "data",
                    {}
                ) or {}
            )

            result = {
                "merge_layer": merge_layer,
                **data
            }
            current = result

            for key in keys:
                if not isinstance(key, (str)) or not key:
                    raise ValueError("'key' must be a non-empty string")
                
                current[key] = {}
                current = current[key]

            return result

        def read_data(
            self,
            **kwargs
        ):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            keys = (
                kwargs.get(
                    "keys",
                    ()
                ) or ()
            )

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            if not keys:
                return (
                    value_cache_storage_manager
                        .read_all_items()
                )

            data = (
                value_cache_storage_manager
                    .get_one_item(
                        keys=keys
                    )
            )

            return (
                data
            )



    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager

# PluginManager()
