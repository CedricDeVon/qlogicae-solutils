__all__ = (
    "PluginManager",
)

_plugin_root = None
_PluginManager = None
_DebugCommandPluginManager = None
_AboutCommandPluginManager = None
_FooterCommandPluginManager = None
_WorkflowCommandPluginManager = None
_WorkspaceCommandPluginManager = None
_FilesystemCommandPluginManager = None
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
            global _AboutCommandPluginManager
            global _WorkspaceCommandPluginManager
            global _FooterCommandPluginManager
            global _WorkflowCommandPluginManager
            global _FilesystemCommandPluginManager
            global _DebugCommandPluginManager
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _plugin_root = (
                _ExternalDependencyManager().get_singleton().import_module(                    
                    path="qlogicae_solutils.v1.plugin.root",
                )
            )
            _AboutCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.about_command_plugin_manager",
                        member="AboutCommandPluginManager",
                        is_member_callable=True,
                    )
            )
            _WorkspaceCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.workspace_command_plugin_manager",
                        member="WorkspaceCommandPluginManager",
                        is_member_callable=True,
                    )
            )
            _FooterCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.footer_command_plugin_manager",
                        member="FooterCommandPluginManager",
                        is_member_callable=True,
                    )
            )
            _WorkflowCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.workflow_command_plugin_manager",
                        member="WorkflowCommandPluginManager",
                        is_member_callable=True,
                    )
            )
            _FilesystemCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.filesystem_command_plugin_manager",
                        member="FilesystemCommandPluginManager",
                        is_member_callable=True,
                    )
            )
            _DebugCommandPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_solutils.v1.library.debug_command_plugin_manager",
                        member="DebugCommandPluginManager",
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

        def read_default_options(self):
            workflow_command_plugin_manager = (
                _WorkflowCommandPluginManager()
                    .get_singleton()
            )
            workspace_command_plugin_manager = (
                _WorkspaceCommandPluginManager()
                    .get_singleton()
            )
            filesystem_command_plugin_manager = (
                _FilesystemCommandPluginManager()
                    .get_singleton()
            )
            about_command_plugin_manager = (
                _AboutCommandPluginManager()
                    .get_singleton()
            )
            debug_command_plugin_manager = (
                _DebugCommandPluginManager()
                    .get_singleton()
            )
            footer_command_plugin_manager = (
                _FooterCommandPluginManager()
                    .get_singleton()
            )

            data = {
                "is_recursive": (
                    True
                ),                    
                "target_filesystem_paths": (
                    "qlogicae/solutils/v1/private/plugin",
                    "qlogicae/solutils/v1/public/plugin",
                ),
                "imported_modules": (
                    _plugin_root(),
                ),
                "raw_export_data": (
                    workflow_command_plugin_manager
                        .plugin_exports,
                    workspace_command_plugin_manager
                        .plugin_exports,
                    filesystem_command_plugin_manager
                        .plugin_exports,
                    about_command_plugin_manager
                        .plugin_exports,
                    debug_command_plugin_manager
                        .plugin_exports,
                    footer_command_plugin_manager
                        .plugin_exports,
                ),
            }

            return data


    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager

