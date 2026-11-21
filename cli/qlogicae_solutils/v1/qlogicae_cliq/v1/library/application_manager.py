__all__ = (
    "ApplicationManager",
)

_ApplicationManager = None
_ExternalDependencyManager = None
_ModuliPluginManager = None


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
            global _ExternalDependencyManager
            global _ModuliPluginManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )            

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError(
                    "'kwargs' must be a dictionary"
                )

            return True

        def shutdown(self):
            return True     

        def run(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            plugin_options = (
                kwargs.get(
                    "plugin_options",
                    {}
                ) or {}
            )            
            plugin_options_setup = (
                plugin_options.get(
                    "setup",
                    {}
                ) or {}
            )
            plugin_options_run = (
                plugin_options.get(
                    "run",
                    {}
                ) or {}
            )

            _ModuliPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_moduli.v1.library.plugin_manager",
                        member="ModuliPluginManager",
                        is_member_callable=True,
                    )
            )
            plugin_manager = (
                _ModuliPluginManager()
                    .get_singleton()
            )

            result = True
            result = (
                plugin_manager.setup(
                    **plugin_options_setup
                ) and result
            )
            result = (
                plugin_manager.run(
                    **plugin_options_run
                ) and result
            )

            return result   


    _ApplicationManager = __ApplicationManager
    _allocate = lambda: None


def ApplicationManager():
    if _ApplicationManager is None:
        _allocate()

    return _ApplicationManager
