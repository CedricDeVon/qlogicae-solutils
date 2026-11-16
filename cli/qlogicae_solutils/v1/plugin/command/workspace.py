__all__ = (
    "export"
)

_data = None


def workspace_setup_command_handler(arguments):
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
                                    "kwargs": { "help": "", },
                                    "subcommands": [
                                        {
                                            "name": "setup",
                                            "kwargs": { "help": "", },
                                            "command_handler": (
                                                workspace_setup_command_handler
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--versions",
                                                        "-v"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "versions",
                                                        "help": "",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
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
    if not _data:
        _allocate()

    return _data
