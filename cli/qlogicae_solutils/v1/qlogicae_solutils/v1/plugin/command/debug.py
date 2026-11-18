__all__ = (
    "export"
)

_data = None


def run_debug_view_value_cache_command(arguments):
    print(
        arguments
    )

    return True


def run_debug_view_plugin_command(arguments):
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
                                    "name": "debug",
                                    "args": (),
                                    "kwargs": { "help": "Manage debug operations.", },
                                    "subcommands": [
                                        {
                                            "name": "show",
                                            "args": (),
                                            "kwargs": { "help": "Display operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "value-cache",
                                                    "args": (),
                                                    "kwargs": { "help": "Display value cache database items.", },
                                                    "command_handler": (
                                                        run_debug_view_value_cache_command
                                                    ),
                                                    "arguments": [
                                                        {
                                                            "args": (
                                                                "--targets",
                                                                "-t"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "targets",
                                                                "help": "Value cache database key paths.",
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
            }
        }
    }

    _allocate = lambda: None


def export():
    if _data is None:
        _allocate()

    return _data

