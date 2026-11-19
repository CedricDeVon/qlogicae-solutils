__all__ = (
    "DebugCommandPluginManager",
)


_ValueCacheStorageManager = None
_DebugCommandPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _DebugCommandPluginManager

    class __DebugCommandPluginManager:
        __slots__ = (
            "_plugin_exports",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def plugin_exports(self):
            return self._plugin_exports


        @plugin_exports.setter
        def plugin_exports(self, value):
            if not isinstance(value, dict):
                raise ValueError(
                    "'plugin_exports' must be a dictionary"
                )

            self._plugin_exports = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ValueCacheStorageManager
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
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

            self._plugin_exports = {
                "object_merge": {
                    "level": 1
                },
                "qlogicae": {
                    "cliq": {
                        "v1": {    
                            "command": {
                                "options": {
                                    "commands": [
                                        {
                                            "name": "debug",
                                            "args": (),
                                            "kwargs": { "help": "Manage debug operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "view",
                                                    "args": (),
                                                    "kwargs": { "help": "Display operations.", },
                                                    "subcommands": [
                                                        {
                                                            "name": "value-cache",
                                                            "args": (),
                                                            "kwargs": { "help": "Display value cache database items.", },
                                                            "command_handler": (
                                                                self.run_debug_view_value_cache_command
                                                            ),
                                                            "arguments": [
                                                                {
                                                                    "args": (
                                                                        "--targets",
                                                                        "-t"
                                                                    ),
                                                                    "kwargs": {
                                                                        "dest": "targets",
                                                                        "help": "Value cache database key paths.",
                                                                        "required": True,
                                                                        "default": (),
                                                                        "type": str,
                                                                        "nargs": "+",
                                                                    }
                                                                }
                                                            ],
                                                        },
                                                    ],
                                                },                                        
                                            ],
                                        },
                                    ],
                                },
                            },
                        }
                    }
                }
            }

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def run_debug_view_value_cache_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            result = True
            targets = (
                (getattr(arguments, "targets", tuple())
                if not isinstance(arguments, tuple)
                else arguments.get("targets", tuple())) or tuple()
            )
            if not targets:
                return result

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            result = (
                value_cache_storage_manager
                    .display_one_item(
                        keys=targets
                    )
            )
            
            return result


    _DebugCommandPluginManager = __DebugCommandPluginManager
    _allocate = lambda: None


def DebugCommandPluginManager():
    if _DebugCommandPluginManager is None:
        _allocate()

    return _DebugCommandPluginManager

