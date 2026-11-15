__all__ = (
    "export"
)

_data = None


def debug_view_value_cache_command_handler(arguments):
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
        "command": {
            "options": {
                "commands": [
                    {
                        "name": "debug",
                        "args": (),
                        "kwargs": { "help": "", },
                        "subcommands": [
                            {
                                "name": "view",
                                "args": (),
                                "kwargs": { "help": "", },
                                "subcommands": [
                                    {
                                        "name": "value-cache",
                                        "kwargs": { "help": "", },
                                        "command_handler": (
                                            debug_view_value_cache_command_handler
                                        ),
                                        "arguments": [
                                            {
                                                "args": (
                                                    "--target",
                                                    "-t"
                                                ),
                                                "kwargs": {
                                                    "dest": "target",
                                                    "help": "",
                                                    "required": True,
                                                    "default": (),
                                                    "type": str,
                                                    "nargs": "+",
                                                }
                                            }
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        },
    }

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data

