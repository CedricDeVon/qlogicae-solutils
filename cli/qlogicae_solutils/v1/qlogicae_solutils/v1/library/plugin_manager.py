__all__ = (
    "PluginManager",
)

_plugin_root = None
_PluginManager = None
_plugin_command_about = None
_plugin_command_debug = None
_plugin_command_footer = None
_plugin_command_workflow = None
_plugin_command_workspace = None
_plugin_command_filesystem = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
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
            global _plugin_root
            global _plugin_command_about
            global _plugin_command_debug
            global _plugin_command_footer
            global _plugin_command_workflow
            global _plugin_command_workspace
            global _plugin_command_filesystem
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager().get_singleton
            )
            _plugin_root = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.root",
                )
            )
            _plugin_command_workspace = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.workspace",
                )
            )
            _plugin_command_workflow = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.workflow",
                )
            )
            _plugin_command_filesystem = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.filesystem",
                )
            )
            _plugin_command_about = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.about",
                )
            )
            _plugin_command_debug = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.debug",
                )
            )
            _plugin_command_footer = (
                _ExternalDependencyManager().import_module(                    
                    path="qlogicae_solutils.v1.plugin.command.footer",
                )
            )

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def read_default_options(self):
            data = {
                "is_recursive": True,                    
                "target_filesystem_paths": (
                    "qlogicae/solutils/v1/private/plugin",
                    "qlogicae/solutils/v1/public/plugin",
                ),
                "imported_modules": (
                    _plugin_root(),
                    _plugin_command_workflow(),
                    _plugin_command_workspace(),                    
                    _plugin_command_filesystem(),
                    _plugin_command_about(),
                    _plugin_command_debug(),
                    _plugin_command_footer(),
                ),
            }

            return data


    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager

