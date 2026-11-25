__all__ = (
    "PluginDataManager",
)

_PluginDataManager = None
_ExternalDependencyManager = None

_ObjectMergeManager = None
_PythonModuleManager = None
_ValueCacheStorageManager = None


def _allocate():
    global _allocate
    global _PluginDataManager

    class __PluginDataManager:
        __slots__ = (
            "_plugin_items",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        def read_plugin_items(self):
            return (
                self._plugin_items
            )

        @property
        def plugin_items(self):
            return self._plugin_items

        @plugin_items.setter
        def plugin_items(self, value):
            if not isinstance(value, (tuple, list)):
                raise TypeError("")

            self._plugin_items = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _ObjectMergeManager
            global _PythonModuleManager
            global _ValueCacheStorageManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
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

            self._plugin_items = []

            return True

        def setup(
            self,
            kwargs,
        ):  
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            kwargs = (
                self.write_setup_kwargs(
                    kwargs
                )
            )

            target_filesystem_paths = (
                kwargs.get("target_filesystem_paths", tuple()) or tuple()
            )

            if not isinstance(target_filesystem_paths, (tuple, list)):
                raise TypeError("")

            is_recursive = (
                kwargs.get("is_recursive", True)
            )
            if not isinstance(is_recursive, (bool)):
                raise TypeError("")

            is_export_call_enabled = (
                kwargs.get("is_export_call_enabled", True)
            )
            if not isinstance(is_export_call_enabled, (bool)):
                raise TypeError("")

            internal_objects = (
                kwargs.get("internal_objects", tuple()) or tuple()
            )
            if not isinstance(internal_objects, (tuple, list)):
                raise TypeError("")

            internal_modules = (
                kwargs.get("internal_modules", tuple()) or tuple()
            )
            if not isinstance(internal_modules, (tuple, list)):
                raise TypeError("")

            external_objects = (
                kwargs.get("external_objects", tuple()) or tuple()
            )
            if not isinstance(external_objects, (tuple, list)):
                raise TypeError("")

            internal_data = (
                kwargs.get("internal_data", tuple()) or tuple()
            )
            if not isinstance(internal_data, (tuple, list)):
                raise TypeError("")

            initial_data = (
                kwargs.get("initial_data", {}) or {}
            )
            if not isinstance(initial_data, (dict)):
                raise TypeError("")

            object_merge_manager = (
                _ObjectMergeManager()
                    .get_singleton()
            )
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
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

            plugin_items = (
                internal_objects +
                internal_modules +
                external_objects +
                external_modules
            )
            if is_export_call_enabled:
                plugin_items = [
                    (plugin_item, self.export_plugin(plugin_item),)
                    for plugin_item in plugin_items
                ]
            else:
                plugin_items = [
                    (plugin_item, {},)
                    for plugin_item in plugin_items
                ]

            plugin_items.sort(
                key=(
                    lambda plugin_item: (
                        ((plugin_item[1] or {}).get('layer', 0) or 0)
                    )
                )
            )

            merged_plugin_export_data = (
                object_merge_manager.deep_merge(
                    value_cache_storage_manager.read_all_data(),
                    initial_data
                )
            )

            if is_export_call_enabled:
                for plugin_item in plugin_items:
                    if not isinstance(plugin_item, (tuple, list)):
                        raise TypeError("")

                    plugin_item_export_data = plugin_item[1]
                    if not isinstance(plugin_item_export_data, (dict)):
                        raise TypeError("")

                    plugin_item_export_data_key_path = (
                        plugin_item_export_data.get(
                            "root_key_path",
                            ""
                        ) or ""
                    )
                    if plugin_item_export_data_key_path in merged_plugin_export_data:
                        merged_plugin_export_data = (
                            object_merge_manager.deep_merge(
                                merged_plugin_export_data,
                                plugin_item_export_data
                            )
                        )
                    else:
                        merged_plugin_export_data[plugin_item_export_data_key_path] = (
                            plugin_item_export_data.get(
                                plugin_item_export_data_key_path,
                                {}
                            ) or {}
                        )

            if merged_plugin_export_data:
                value_cache_storage_manager.write_all_data(
                    merged_plugin_export_data
                )

            self._plugin_items = [
                plugin_item[0]
                for plugin_item in plugin_items
            ]

            return True

        def shutdown(self):
            return True

        def read_all_data(
            self,
            root_key_path
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            data = (
                value_cache_storage_manager
                    .read_one_data(
                        key_path=(root_key_path,)
                    )
            )

            return (
                data
            )

        def read_one_data(
            self,
            root_key_path,
            key_path,
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            data = (
                value_cache_storage_manager
                    .read_one_data(
                        key_path=(root_key_path, *key_path,)
                    )
            )

            return (
                data
            )

        def write_all_data(
            self,
            root_key_path,
            value
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                value_cache_storage_manager
                    .write_one_data(
                        key_path=(root_key_path,),
                        value=value
                    ) and result
            )

            return (
                result
            )

        def write_one_data(
            self,
            root_key_path,
            key_path,
            value,
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                value_cache_storage_manager
                    .write_one_data(
                        key_path=(root_key_path, *key_path,),
                        value=value
                    ) and result
            )

            return (
                result
            )

        def remove_one_data(
            self,
            root_key_path,
            key_path,
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                value_cache_storage_manager
                    .remove_one_data(
                        key_path=(root_key_path, *key_path,),
                    ) and result
            )

            return (
                result
            )

        def remove_all_data(
            self,
            root_key_path,
        ):
            if not isinstance(root_key_path, (str)):
                raise TypeError("")

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            result = True
            result = (
                value_cache_storage_manager
                    .remove_one_data(
                        key_path=(root_key_path,),
                    ) and result
            )

            return (
                result
            )

        def write_setup_kwargs(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            if "target_filesystem_paths" not in kwargs:
                kwargs["target_filesystem_paths"] = tuple()

            if "is_recursive" not in kwargs:
                kwargs["is_recursive"] = True

            if "is_export_call_enabled" not in kwargs:
                kwargs["is_export_call_enabled"] = True

            if "internal_objects" not in kwargs:
                kwargs["internal_objects"] = tuple()

            if "internal_modules" not in kwargs:
                kwargs["internal_modules"] = tuple()

            if "external_objects" not in kwargs:
                kwargs["external_objects"] = tuple()

            if "internal_data" not in kwargs:
                kwargs["internal_data"] = {}

            return kwargs

        def setup_plugin_data(
            self,
            kwargs
        ):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            layer = (
                kwargs.get(
                    "layer",
                    0
                ) or 0
            )
            root_key_path = (
                kwargs.get(
                    "root_key_path",
                    ""
                ) or ""
            )
            data = (
                kwargs.get(
                    "data",
                    {}
                ) or {}
            )

            result = {
                "root_key_path": root_key_path,
                "layer": layer,
                root_key_path: data,
            }

            return result

        def export_plugin(
            self,
            plugin_item,
        ):
            if not plugin_item:
                raise TypeError("")

            result = True
            plugin_method = (
                getattr(
                    plugin_item,
                    "export_plugin"
                ) or None
            )
            if plugin_method:
                if not callable(plugin_method):
                    raise TypeError("")
                
                result = (
                    plugin_method()
                )

            return (
                result
            )


    _PluginDataManager = __PluginDataManager
    _allocate = lambda: None


def PluginDataManager():
    if _PluginDataManager is None:
        _allocate()

    return _PluginDataManager

# PluginDataManager()
