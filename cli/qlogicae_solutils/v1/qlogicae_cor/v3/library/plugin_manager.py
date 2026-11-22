__all__ = (
    "PluginManager",
)

_PluginManager = None
_ExternalDependencyManager = None

_ObjectMergeManager = None
_PythonModuleManager = None
_ValueCacheStorageManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
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

        @property
        def plugin_items(self):
            return self._plugin_items

        @plugin_items.setter
        def plugin_items(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

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

            self._plugin_items = tuple()

            return True

        def setup(
            self,
            **kwargs,
        ):        
            kwargs = (
                self.write_setup_kwargs(
                    kwargs
                )
            )

            target_filesystem_paths = (
                kwargs.get("target_filesystem_paths", tuple()) or tuple()
            )
            if not isinstance(target_filesystem_paths, (tuple, list)):
                raise ValueError("")

            is_recursive = (
                kwargs.get("is_recursive", True)
            )
            if not isinstance(is_recursive, (bool)):
                raise ValueError("")

            is_export_call_enabled = (
                kwargs.get("is_export_call_enabled", True)
            )
            if not isinstance(is_export_call_enabled, (bool)):
                raise ValueError("")

            internal_objects = (
                kwargs.get("internal_objects", tuple()) or tuple()
            )
            if not isinstance(internal_objects, (tuple, list)):
                raise ValueError("")

            internal_modules = (
                kwargs.get("internal_modules", tuple()) or tuple()
            )
            if not isinstance(internal_modules, (tuple, list)):
                raise ValueError("")

            external_objects = (
                kwargs.get("external_objects", tuple()) or tuple()
            )
            if not isinstance(external_objects, (tuple, list)):
                raise ValueError("")

            internal_data = (
                kwargs.get("internal_data", tuple()) or tuple()
            )
            if not isinstance(internal_data, (tuple, list)):
                raise ValueError("")

            initial_data = (
                kwargs.get("initial_data", {}) or {}
            )
            if not isinstance(initial_data, (dict)):
                raise ValueError("")

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
                        ((plugin_item[1] or {}).get('moduli', {}) or {})
                            .get("layer", 0) or 0
                    )
                )
            )

            merged_plugin_export_data = (
                object_merge_manager.deep_merge(
                    self.read_all_items(),
                    initial_data
                )
            )

            if is_export_call_enabled:
                for plugin_item in plugin_items:
                    if not isinstance(plugin_item, (dict)):
                        raise ValueError("")

                    plugin_item_export_data = plugin_item[1]
                    if not isinstance(plugin_item_export_data, (dict)):
                        raise ValueError("")

                    merged_plugin_export_data = (
                        object_merge_manager.deep_merge(
                            merged_plugin_export_data,
                            plugin_item_export_data
                        )
                    )

            if merged_plugin_export_data:
                value_cache_storage_manager.set_all_items(
                    values=merged_plugin_export_data
                )

            self._plugin_items = (
                plugin_item[0]
                for plugin_item in plugin_items
            )

            return result

        def shutdown(self):
            return True

        def run(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("")

            if not self._plugin_items:
                return True

            is_setup_enabled = (
                kwargs.get("is_setup_enabled", True)
            )
            is_run_enabled = (
                kwargs.get("is_run_enabled", True)
            )
            is_shutdown_enabled = (
                kwargs.get("is_shutdown_enabled", False)
            )

            result = True

            if is_setup_enabled:
                result = (
                    self.setup_plugins() and result
                )

            if is_run_enabled:
                result = (
                    self.run_plugins() and result
                )

            if is_shutdown_enabled:
                result = (
                    self.shutdown_plugins() and result
                )

            return result
    
        def write_setup_kwargs(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("")

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

            if "initial_data" not in kwargs:
                kwargs["initial_data"] = {}

            return kwargs

        def read_all_items(
            self,
        ):
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            return (
                value_cache_storage_manager
                    .read_all_items()
            )

        def setup_plugins(self):
            return (
                self.run_method_plugins(
                    self.setup_plugin
                )
            )

        def run_plugins(self):
            return (
                self.run_method_plugins(
                    self.run_plugin
                )
            )

        def shutdown_plugins(self):
            return (
                self.run_method_plugins(
                    self.shutdown_plugin
                )
            )

        def run_method_plugins(
            self,
            callback,
        ):
            if not self._plugin_items:
                return True

            result = True
            for plugin_item in self._plugin_items:
                if not plugin_item:
                    raise ValueError("")

                result = (
                    callback(
                        plugin_item
                    )
                )

            return result

        def export_plugin(
            self,
            plugin_item,
        ):
            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "export_plugin"
                )
            )

        def setup_plugin(
            self,
            plugin_item,
        ):
            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "setup_plugin"
                )
            )

        def run_plugin(
            self,
            plugin_item,
        ):
            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "run_plugin"
                )
            )

        def shutdown_plugin(
            self,
            plugin_item,
        ):
            return (
                self.run_optional_plugin_method(
                    plugin_item,
                    "shutdown_plugin"
                )
            )

        def run_optional_plugin_method(
            self,            
            plugin_item,
            method_name,
        ):
            if not plugin_item:
                raise ValueError("")

            if isinstance(method_name, (str)):
                raise ValueError("")

            result = True
            plugin_method = (
                getattr(
                    plugin_item,
                    method_name
                ) or None
            )
            if plugin_method:
                if not callable(plugin_method):
                    raise ValueError("")
                
                result = (
                    plugin_method() and result
                )

            return (
                result
            )

        def setup_data(
            self,
            **kwargs
        ):
            if not isinstance(kwargs, (dict)):
                raise ValueError("")

            options = (
                kwargs.get(
                    "moduli",
                    {}
                ) or {}
            )
            key_path = (
                kwargs.get(
                    "key_path",
                    ()
                ) or ()
            )
            data = (
                kwargs.get(
                    "data",
                    {}
                ) or {}
            )

            result = {
                "moduli": {
                    **options
                },
                **data
            }
            current = result

            for key in key_path:
                if not isinstance(key, (str)) or not key:
                    raise ValueError("")
                
                current[key] = {}
                current = current[key]

            return result

        def read_data(
            self,
            **kwargs
        ):
            if not isinstance(kwargs, (dict)):
                raise ValueError("")

            key_path = (
                kwargs.get(
                    "key_path",
                    ()
                ) or ()
            )


            if not key_path:
                return (
                    self.read_all_items()
                )

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )
            data = (
                value_cache_storage_manager
                    .get_one_item(
                        keys=key_path
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
