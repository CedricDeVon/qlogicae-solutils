__all__ = (
    "export"
)

_data = None


def run_workspace_setup_template_command(arguments):
    from qlogicae_cor.v3.library.system_manager import (
        SystemManager
    )
    from qlogicae_cor.v3.library.filesystem_manager import (
        FilesystemManager
    )
    from qlogicae_cor.v3.library.file_entity_filesystem_tree_setup_options import (
        FileEntityFilesystemTreeSetupOptions
    )
    from qlogicae_cor.v3.library.folder_entity_filesystem_tree_setup_options import (
        FolderEntityFilesystemTreeSetupOptions
    )

    _SystemManager = (
        SystemManager()
    )
    _FilesystemManager = (
        FilesystemManager()
    )
    _FileEntityFilesystemTreeSetupOptions = (
        FileEntityFilesystemTreeSetupOptions()
    )
    _FolderEntityFilesystemTreeSetupOptions = (
        FolderEntityFilesystemTreeSetupOptions()
    )

    targets = (
        (getattr(arguments, "targets", tuple())
        if not isinstance(arguments, tuple)
        else arguments.get("targets", tuple())) or tuple()
    )
    for target in targets:
        if target is None:
            continue

        if target == "init":
            print(target)

            _FilesystemManager.get_singleton().setup_filesystem_tree(
                _SystemManager.get_singleton().current_executing_console_filesystem_path,
                [
                    _FolderEntityFilesystemTreeSetupOptions(
                        name="qlogicae",
                        entities=[
                            _FolderEntityFilesystemTreeSetupOptions(
                                name="solutils",
                                entities=[
                                    _FolderEntityFilesystemTreeSetupOptions(
                                        name="v1",
                                        entities=[
                                            _FolderEntityFilesystemTreeSetupOptions(
                                                name="private",
                                                entities=[
                                                    _FileEntityFilesystemTreeSetupOptions(
                                                        name=".gitignore",
                                                        content="*",
                                                    ),
                                                    _FolderEntityFilesystemTreeSetupOptions(
                                                        name="plugin",
                                                        entities=[
                                                            _FileEntityFilesystemTreeSetupOptions(
                                                                name="__init__.py",
                                                            ),
                                                            _FileEntityFilesystemTreeSetupOptions(
                                                                name="root.py",
                                                                content="""
def export():
    return {}
"""
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                            _FolderEntityFilesystemTreeSetupOptions(
                                                name="public",
                                                entities=[
                                                    _FolderEntityFilesystemTreeSetupOptions(
                                                        name="plugin",
                                                        entities=[
                                                            _FileEntityFilesystemTreeSetupOptions(
                                                                name="__init__.py",
                                                            ),
                                                            _FileEntityFilesystemTreeSetupOptions(
                                                                name="root.py",
                                                                content="""
def export():
    return {}
"""
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),                        
                        ]
                    ),
                ]
            )

    return True


def _allocate():
    global _allocate
    global _data

    _data = {
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
                                            "name": "setup",
                                            "args": (),
                                            "kwargs": { "help": "Setup operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "template",
                                                    "args": (),
                                                    "kwargs": { "help": "Apply templates.", },
                                                    "command_handler": (
                                                        run_workspace_setup_template_command
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
                                    ],
                                },
                            ],
                        },
                    },
                }
            }
        }
    }

    _allocate = lambda: None


def export():
    if _data is None:
        _allocate()

    return _data
