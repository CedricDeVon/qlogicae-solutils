__all__ = (
    "WorkspaceCommandPluginManager",
)

_SystemManager = None
_FilesystemTreeManager = None
_FileEntityFilesystemTreeSetupOptions = None
_FolderEntityFilesystemTreeSetupOptions = None
_WorkspaceCommandPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _WorkspaceCommandPluginManager

    class __WorkspaceCommandPluginManager:
        __slots__ = (
            "_plugin_exports",
            "_template_targets",
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

        @property
        def template_targets(self):
            return self._template_targets

        @template_targets.setter
        def template_targets(self, value):
            if not isinstance(value, dict):
                raise ValueError(
                    "'template_targets' must be a dictionary"
                )

            self._template_targets = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _SystemManager
            global _FilesystemTreeManager
            global _FileEntityFilesystemTreeSetupOptions
            global _FolderEntityFilesystemTreeSetupOptions
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _SystemManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.system_manager",
                        member="SystemManager",
                        is_member_callable=True,
                    )
            )
            _FilesystemTreeManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.filesystem_tree_manager",
                        member="FilesystemTreeManager",
                        is_member_callable=True,
                    )
            )
            _FileEntityFilesystemTreeSetupOptions = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.file_entity_filesystem_tree_setup_options",
                        member="FileEntityFilesystemTreeSetupOptions",
                        is_member_callable=True,
                    )
            )
            _FolderEntityFilesystemTreeSetupOptions = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.folder_entity_filesystem_tree_setup_options",
                        member="FolderEntityFilesystemTreeSetupOptions",
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
                                            "name": "workspace",
                                            "args": (),
                                            "kwargs": { "help": "Manage workspace operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "apply",
                                                    "args": (),
                                                    "kwargs": { "help": "Apply operations.", },
                                                    "subcommands": [
                                                        {
                                                            "name": "template",
                                                            "args": (),
                                                            "kwargs": { "help": "Apply templates.", },
                                                            "command_handler": (
                                                                self.run_workspace_setup_template_command
                                                            ),
                                                            "arguments": [
                                                                {
                                                                    "args": (
                                                                        "--targets",
                                                                        "-t"
                                                                    ),
                                                                    "kwargs": {
                                                                        "dest": "targets",
                                                                        "help": "Template targets.",
                                                                        "required": True,
                                                                        "default": (),
                                                                        "type": str,
                                                                        "nargs": "+",
                                                                    }
                                                                },
                                                            ]
                                                        },                                                
                                                    ],
                                                },
                                                {
                                                    "name": "show",
                                                    "args": (),
                                                    "kwargs": { "help": "Display operations.", },
                                                    "subcommands": [
                                                        {
                                                            "name": "templates",
                                                            "args": (),
                                                            "kwargs": { "help": "Display list of templates.", },
                                                            "command_handler": (
                                                                self.run_workspace_show_templates_command
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
            self._template_targets = {
                "v1-init": self.run_template_target_v1_init
            }

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True

        def run_workspace_show_templates_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            for key, _value in self._template_targets.items():
                if not key:
                    continue

                print(key)

            return True

        def run_workspace_setup_template_command(self, arguments):
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
            
            for target in targets:
                if not target:
                    continue

                command = (
                    self._template_targets
                        .get(
                            target,
                            None
                        ) or None
                )
                if not command or not callable(command):
                    continue

                result = command() and result

            return result

        def run_template_target_v1_init(self):
            system_manager = (
                _SystemManager().get_singleton()
            )
            filesystem_tree_manager = (
                _FilesystemTreeManager().get_singleton()
            )
            FileEntityFilesystemTreeSetupOptions = (
                _FileEntityFilesystemTreeSetupOptions()
            )
            FolderEntityFilesystemTreeSetupOptions = (
                _FolderEntityFilesystemTreeSetupOptions()
            )
            
            default_plugin_file_content = """
def export():
    return {}
"""          

            gitignore_filesystem = (
                FileEntityFilesystemTreeSetupOptions(
                    name=".gitignore",
                    content="*",
                )
            )
            plugin_filesystem = (
                FolderEntityFilesystemTreeSetupOptions(
                    name="plugin",
                    entities=(
                        FileEntityFilesystemTreeSetupOptions(
                            name="__init__.py",
                        ),
                        FileEntityFilesystemTreeSetupOptions(
                            name="root.py",
                            content=default_plugin_file_content
                        ),
                    )
                )
            )
            private_filesystem = (
                FolderEntityFilesystemTreeSetupOptions(
                    name="private",
                    entities=(
                        gitignore_filesystem,
                        plugin_filesystem,
                    )
                )
            )
            public_filesystem = (
                FolderEntityFilesystemTreeSetupOptions(
                    name="public",
                    entities=(
                        plugin_filesystem,
                    )
                )
            )

            result = True
            result = filesystem_tree_manager.setup_filesystem_tree(
                system_manager.current_executing_console_filesystem_path,
                (
                    FolderEntityFilesystemTreeSetupOptions(
                        name="qlogicae",
                        entities=(
                            FolderEntityFilesystemTreeSetupOptions(
                                name="solutils",
                                entities=(
                                    FolderEntityFilesystemTreeSetupOptions(
                                        name="v1",
                                        entities=(
                                            private_filesystem,
                                            public_filesystem,
                                        )
                                    ),
                                )
                            ),                        
                        )
                    ),
                )
            ) and result

            return result


    _WorkspaceCommandPluginManager = __WorkspaceCommandPluginManager
    _allocate = lambda: None


def WorkspaceCommandPluginManager():
    if _WorkspaceCommandPluginManager is None:
        _allocate()

    return _WorkspaceCommandPluginManager

