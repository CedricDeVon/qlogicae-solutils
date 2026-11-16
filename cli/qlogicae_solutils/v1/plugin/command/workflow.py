__all__ = (
    "export"
)

_data = None


def workflow_run_command_handler(arguments):
    print(
        arguments
    )

    return True


def workflow_list_selections_command_handler(arguments):
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
                                    "name": "workflow",
                                    "args": (),
                                    "kwargs": { "help": "", },
                                    "subcommands": [
                                        {
                                            "name": "run",
                                            "kwargs": { "help": "", },
                                            "command_handler": (
                                                workflow_run_command_handler
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--selections",
                                                        "-s"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "selections",
                                                        "help": "",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                }
                                            ],
                                        },
                                        {
                                            "name": "list",
                                            "kwargs": { "help": "", },
                                            "subcommands": [
                                                {
                                                    "name": "selections",
                                                    "kwargs": { "help": "", },
                                                    "command_handler": (
                                                        workflow_list_selections_command_handler
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

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data

