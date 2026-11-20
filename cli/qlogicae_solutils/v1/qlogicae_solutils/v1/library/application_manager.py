__all__ = (
    "ApplicationManager",
)

_PluginManager = None
_ApplicationManager = None
_CliApplicationManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _ApplicationManager

    class __ApplicationManager:
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
            global _PluginManager
            global _CliApplicationManager            
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _PluginManager = (
                _ExternalDependencyManager().get_singleton().import_module(                    
                    path="qlogicae_solutils.v1.library.plugin_manager",
                    member="PluginManager",
                    is_member_callable=True,
                )
            )
            _CliApplicationManager = (
                _ExternalDependencyManager().get_singleton().import_module(                    
                    path="qlogicae_cliq.v1.library.cli_application_manager",
                    member="CliApplicationManager",
                    is_member_callable=True,
                )
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def run(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            cli_application_manager = (
                _CliApplicationManager().get_singleton()
            )
            plugin_manager = (
                _PluginManager().get_singleton()
            )
            external_dependency_options = {
                "is_pre_allocated": False,
            }
            plugin_options = (
                plugin_manager
                    .read_default_options()
            )

            result = cli_application_manager.run(
                external_dependency=(
                    external_dependency_options
                ),
                plugin=(
                    plugin_options
                ),
            )

            return result


    _ApplicationManager = __ApplicationManager
    _allocate = lambda: None


def ApplicationManager():
    if _ApplicationManager is None:
        _allocate()

    return _ApplicationManager

