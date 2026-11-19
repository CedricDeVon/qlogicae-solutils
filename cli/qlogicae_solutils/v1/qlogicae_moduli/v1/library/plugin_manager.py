__all__ = (
    "PluginManager",
)

_types = None
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
            global _types

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager().get_singleton
            )

            _types = (
                _ExternalDependencyManager().import_module(
                    path="types",
                )
            )
            _ObjectMergeManager = (
                _ExternalDependencyManager().import_module(
                    path="qlogicae_cor.v3.library.object_merge_manager",
                    member="ObjectMergeManager",
                    is_member_callable=True,
                )
            )
            _PythonModuleManager = (
                _ExternalDependencyManager().import_module(
                    path="qlogicae_cor.v3.library.python_module_manager",
                    member="PythonModuleManager",
                    is_member_callable=True,
                )
            )
            _ValueCacheStorageManager = (
                _ExternalDependencyManager().import_module(
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

            imported_modules = (
                self.read_imported_modules(
                    kwargs
                )
            )
            raw_module_exports = (
                self.read_raw_module_exports(
                    imported_modules
                )
            )

            self.setup_merged_raw_module_exports(
                kwargs,
                raw_module_exports
            )

            return True

        def shutdown(self):
            return True

        def read_module_exports(
            self,
        ):
            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            return (
                value_cache_storage_manager.read_all_items()
            )

        def read_imported_modules(
            self,
            options,
        ):
            if not isinstance(options, (dict)) or not options:
                raise ValueError("'options' must be a non-empty dictionary")

            target_filesystem_paths = (
                options.get("target_filesystem_paths", tuple()) or tuple()
            )
            is_recursive = (
                options.get("is_recursive", True)
            )
            imported_modules = (
                options.get("imported_modules", tuple()) or tuple()
            )

            output_imported_modules = tuple(
                _PythonModuleManager()
                    .get_singleton()
                    .read_imported_modules(
                        target_filesystem_paths,
                        is_recursive
                    )
            )

            outputs = (
                imported_modules + output_imported_modules
            )

            return (
                outputs
            )

        def read_raw_module_exports(
            self,
            targets
        ):
            if not isinstance(targets, (tuple, list)) or not targets:
                raise ValueError("'targets' must either be a non-empty tuple or list")

            raw_module_exports = [
                self.read_plugin_module_export(
                    imported_module
                ) for imported_module in targets
            ]

            raw_module_exports.sort(
                key=lambda item: (item.get('object_merge', {}) or {}).get('level', 0)
            )

            return tuple(
                raw_module_exports
            )

        def setup_merged_raw_module_exports(
            self,
            options,
            targets
        ):
            if not isinstance(options, (dict)):
                raise ValueError("'options' must be a dictionary")

            if not isinstance(targets, (tuple, list)) or not targets:
                raise ValueError("'targets' must either be a non-empty tuple or list")

            object_merge_manager = (
                _ObjectMergeManager().get_singleton()
            )
            value_cache_storage_manager = (
                _ValueCacheStorageManager().get_singleton()
            )

            raw_export_data = (
                options.get("raw_export_data", tuple()) or tuple()
            )
            initial_export_data = (
                options.get("initial_export_data", {}) or {}
            )

            targets = (
                tuple(targets) + raw_export_data
            )

            module_exports = (
                object_merge_manager.deep_merge(
                    self.read_module_exports(),
                    initial_export_data
                )
            )
            for target in targets:
                if not isinstance(target, (dict)):
                    raise ValueError("'target' must be a dictionary")

                module_exports = (
                    object_merge_manager.deep_merge(
                        module_exports,
                        target
                    )
                )

            value_cache_storage_manager.set_all_items(
                values=module_exports
            )

            return True

        def read_plugin_module_export(
            self,
            target,
        ):
            if not isinstance(target, (_types().ModuleType)) or not target:
                raise ValueError("'target' must be a non-empty module")

            module_export = (
                target.export()
            )

            return (
                module_export
            )

    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager

# PluginManager()
