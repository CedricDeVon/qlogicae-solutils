__all__ = (
    "export"
)

_data = None


def run_workspace_setup_template_command(arguments):
    print(
        arguments
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
                                                                "--name",
                                                                "-n"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "name",
                                                                "help": "Template name.",
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
