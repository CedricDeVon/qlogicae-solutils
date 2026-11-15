__all__ = (
    "export"
)

_data = None


def filesystem_create_command_handler(arguments):
    print(
        arguments
    )

    return True


def filesystem_remove_command_handler(arguments):
    print(
        arguments
    )

    return True


def filesystem_move_command_handler(arguments):
    print(
        arguments
    )

    return True


def filesystem_copy_command_handler(arguments):
    print(
        arguments
    )

    return True


def filesystem_compress_command_handler(arguments):
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
                        "name": "filesystem",
                        "args": (),
                        "kwargs": { "help": "", },
                        "subcommands": [
                            {
                                "name": "create",
                                "kwargs": { "help": "", },
                                "command_handler": (
                                    filesystem_create_command_handler
                                ),
                                "arguments": [
                                    {
                                        "args": (
                                            "--target-filesystem-path",
                                            "-tfp"
                                        ),
                                        "kwargs": {
                                            "dest": "target_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                ],
                            },
                            {
                                "name": "remove",
                                "kwargs": { "help": "", },
                                "command_handler": (
                                    filesystem_remove_command_handler
                                ),
                                "arguments": [
                                    {
                                        "args": (
                                            "--target-filesystem-path",
                                            "-tfp"
                                        ),
                                        "kwargs": {
                                            "dest": "target_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                ],
                            },
                            {
                                "name": "move",
                                "kwargs": { "help": "", },
                                "command_handler": (
                                    filesystem_move_command_handler
                                ),
                                "arguments": [
                                    {
                                        "args": (
                                            "--input-filesystem-path",
                                            "-ifp"
                                        ),
                                        "kwargs": {
                                            "dest": "input_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                    {
                                        "args": (
                                            "--output-filesystem-path",
                                            "-ofp"
                                        ),
                                        "kwargs": {
                                            "dest": "output_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                ],
                            },
                            {
                                "name": "copy",
                                "kwargs": { "help": "", },
                                "command_handler": (
                                    filesystem_copy_command_handler
                                ),
                                "arguments": [
                                    {
                                        "args": (
                                            "--input-filesystem-path",
                                            "-ifp"
                                        ),
                                        "kwargs": {
                                            "dest": "input_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                    {
                                        "args": (
                                            "--output-filesystem-path",
                                            "-ofp"
                                        ),
                                        "kwargs": {
                                            "dest": "output_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                ],
                            },
                            {
                                "name": "compress",
                                "kwargs": { "help": "", },
                                "command_handler": (
                                    filesystem_compress_command_handler
                                ),
                                "arguments": [
                                    {
                                        "args": (
                                            "--input-filesystem-path",
                                            "-ifp"
                                        ),
                                        "kwargs": {
                                            "dest": "input_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                    {
                                        "args": (
                                            "--output-filesystem-path",
                                            "-ofp"
                                        ),
                                        "kwargs": {
                                            "dest": "output_filesystem_path",
                                            "help": "",
                                            "required": True,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                    {
                                        "args": (
                                            "--excluded-filesystem-path",
                                            "-efp"
                                        ),
                                        "kwargs": {
                                            "dest": "excluded_filesystem_path",
                                            "help": "",
                                            "required": False,
                                            "default": (),
                                            "type": str,
                                            "nargs": "+",
                                        }
                                    },
                                    {
                                        "args": (
                                            "--format",
                                            "-f"
                                        ),
                                        "kwargs": {
                                            "dest": "format",
                                            "help": "",
                                            "required": False,
                                            "default": "zip",
                                            "type": str,
                                        }
                                    },
                                    {
                                        "args": (
                                            "--type",
                                            "-t"
                                        ),
                                        "kwargs": {
                                            "dest": "type",
                                            "help": "",
                                            "required": False,
                                            "default": "deflated",
                                            "type": str,
                                        }
                                    },
                                    {
                                        "args": (
                                            "--level",
                                            "-l"
                                        ),
                                        "kwargs": {
                                            "dest": "level",
                                            "help": "",
                                            "required": False,
                                            "default": 6,
                                            "type": int,
                                        }
                                    },
                                    {
                                        "args": (
                                            "--is-zip-64-allowed",
                                            "-iz64a"
                                        ),
                                        "kwargs": {
                                            "dest": "is_zip_64_allowed",
                                            "help": "",
                                            "required": False,
                                            "default": True,
                                            "type": bool,
                                        }
                                    },
                                    {
                                        "args": (
                                            "--is-timestamp-strict",
                                            "-its"
                                        ),
                                        "kwargs": {
                                            "dest": "is_timestamp_strict",
                                            "help": "",
                                            "required": False,
                                            "default": True,
                                            "type": bool,
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

    _allocate = lambda: None


def export():
    if not _data:
        _allocate()

    return _data
