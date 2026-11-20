__all__ = (
    "PluginManager",
)

_PluginManager = None
_ModuliPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
        __slots__ = (
            "_data_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def data_path(self):
            return self._data_path

        @data_path.setter
        def data_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError(
                    "'value' must be a tuple or list"
                )

            self._data_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ModuliPluginManager
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _ModuliPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_moduli.v1.library.plugin_manager",
                        member="PluginManager",
                        is_member_callable=True,
                    )
            )

            self._data_path = (
                "qlogicae",
                "cliq",
                "v1",
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            return True

        def shutdown(self):
            return True

        def export(self):
            moduli_plugin_manager = (
                _ModuliPluginManager()
                    .get_singleton()
            )
            
            initial_data = (
                moduli_plugin_manager
                    .setup_data(
                        keys=self._data_path,
                        merge_layer=0,
                        data={
                            "database": {
                                "is_enabled": False,
                                "value_cache": {
                                    "is_enabled": False,
                                    "options": {
                                        "values": {},
                                        "defaults": {}
                                    },
                                    "callbacks": {
                                        "on_pre_setup": None,
                                        "on_post_setup": None,
                                    },
                                },
                                "persistent_cache": {
                                    "is_enabled": False,
                                    "options": {
                                        "database_path": "persistent_cache.db",
                                        "create_missing": True,
                                        "lifespan_in_seconds": 0.0,
                                        "file_mode": 0o600,
                                        "key_encoding": "utf-8",
                                        "auto_remove_expired": True,
                                        "auto_remove_invalid": True,
                                        "sync_on_write": False,
                                    },
                                    "callbacks": {
                                        "on_pre_setup": None,
                                        "on_post_setup": None,
                                    },
                                },
                                "callbacks": {
                                    "on_pre_setup": None,
                                    "on_post_setup": None,
                                },
                            },
                            "log": {
                                "is_enabled": False,
                                "file": {
                                    "options": {
                                        "is_enabled": False,
                                        "is_verbose_enabled": True,
                                        "log_level": 10,
                                        "stack_level": 3,
                                        "target_filesystem_paths": [
                                            "logs.log"
                                        ],
                                    },
                                    "callbacks": {
                                        "on_pre_setup": None,
                                        "on_post_setup": None,
                                    },
                                },
                                "console": {
                                    "options": {
                                        "is_enabled": False,
                                        "is_verbose_enabled": True,
                                        "log_level": 10,
                                        "stack_level": 3,
                                    },
                                    "callbacks": {
                                        "on_pre_setup": None,
                                        "on_post_setup": None,
                                    },
                                },
                                "callbacks": {
                                    "on_pre_setup": None,
                                    "on_post_setup": None,
                                },
                            },
                        },
                    )
            )

            return initial_data

        def read_data(self):
            moduli_plugin_manager = (
                _ModuliPluginManager()
                    .get_singleton()
            )

            return (
                moduli_plugin_manager
                    .read_data(
                        keys=self._data_path,
                    )
            )


    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager



# PluginManager()


# def is_log_enabled(self, kwargs):
#     if not isinstance(kwargs, (dict)) or not kwargs:
#         raise ValueError("'kwargs' must be a non-empty dictionary")

#     log_data = (
#         (kwargs.get("log", {}) or {})
#     )
#     is_log_enabled = (
#         log_data.get(
#             "is_enabled",
#             False
#         )
#     )
#     is_console_log_enabled = (
#         ((log_data.get(
#             "console",
#             {}
#         ) or {}).get(
#             "options",
#             {}
#         ) or {}).get(
#             "is_enabled",
#             False
#         )
#     )
#     is_file_log_enabled = (
#         ((log_data.get(
#             "file",
#             {}
#         ) or {}).get(
#             "options",
#             {}
#         ) or {}).get(
#             "is_enabled",
#             False
#         )
#     )

#     return (
#         is_log_enabled or (
#             is_console_log_enabled or
#             is_file_log_enabled
#         )
#     )

# def is_database_enabled(self, kwargs):
#     if not isinstance(kwargs, (dict)) or not kwargs:
#         raise ValueError("'kwargs' must be a non-empty dictionary")

#     database_data = (
#         (kwargs.get("database", {}) or {})
#     )
#     is_database_enabled = (
#         database_data.get(
#             "is_enabled",
#             False
#         )
#     )
#     is_value_cache_database_enabled = (
#         (database_data.get(
#             "value_cache",
#             {}
#         ) or {}).get(
#             "is_enabled",
#             False
#         )
#     )
#     is_persistent_cache_database_enabled = (
#         (database_data.get(
#             "persistent_cache",
#             {}
#         ) or {}).get(
#             "is_enabled",
#             False
#         )
#     )

#     return (
#         is_database_enabled or (
#             is_value_cache_database_enabled or
#             is_persistent_cache_database_enabled
#         )
#     )

# def write_setup_kwargs(self, kwargs):
#     if not isinstance(kwargs, (dict)):
#         raise ValueError("'kwargs' must be a dictionary")

#     if "initial_export_data" not in kwargs:
#         kwargs["initial_export_data"] = (
#             self._raw_export_data
#         )

#     return kwargs

# def read_module_exports(self):
#     _PluginManager = (
#         _ExternalDependencyManager().import_module(
#             path="qlogicae_moduli.v1.library.plugin_manager",
#             member="PluginManager",
#             is_member_callable=True,
#         )
#     )

#     plugin_manager = (
#         _PluginManager()
#             .get_singleton()
#     )

#     data = (
#         plugin_manager.read_module_exports() or {}
#     )

#     return data
