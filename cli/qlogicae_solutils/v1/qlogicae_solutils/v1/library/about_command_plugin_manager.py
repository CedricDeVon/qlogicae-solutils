__all__ = (
    "AboutCommandPluginManager",
)


_ValueCacheStorageManager = None
_AboutCommandPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _AboutCommandPluginManager

    class __AboutCommandPluginManager:
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
                                            "name": "about",
                                            "args": (),
                                            "kwargs": { "help": "Manage application build operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "show",
                                                    "args": (),
                                                    "kwargs": { "help": "Display operations.", },
                                                    "subcommands": [
                                                        {
                                                            "name": "version",
                                                            "args": (),
                                                            "kwargs": { "help": "Show version label.", },
                                                            "command_handler": (
                                                                self.run_about_show_version_command
                                                            ),
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

        def run_about_show_version_command(self, arguments):                
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            value_cache_storage_manager = (
                _ValueCacheStorageManager()
                    .get_singleton()
            )

            print(
                value_cache_storage_manager
                    .get_one_item(keys=(
                        "qlogicae",
                        "solutils",
                        "v1",
                        "current-version-label",
                    )
                )
            )

            return True


    _AboutCommandPluginManager = __AboutCommandPluginManager
    _allocate = lambda: None


def AboutCommandPluginManager():
    if _AboutCommandPluginManager is None:
        _allocate()

    return _AboutCommandPluginManager

