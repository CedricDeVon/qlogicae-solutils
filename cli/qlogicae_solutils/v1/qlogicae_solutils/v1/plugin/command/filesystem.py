__all__ = (
    "export"
)

_data = None


def run_filesystem_create_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_remove_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_move_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_copy_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_compress_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_size_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_list_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_count_command(arguments):
    print(
        arguments
    )

    return True


def run_filesystem_metadata_command(arguments):
    print(
        arguments
    )

    return True


def _allocate():
    global _allocate
    global _data

    default_cli_options = (
        {
            "args": (
                "--is-failure-ignored",
                "-ifi"
            ),
            "kwargs": {
                "dest": "is_failure_ignored",
                "help": "Is failure ignored or not.",
                "required": False,
                "default": True,
                "type": bool,
            }
        },                                                
        {
            "args": (
                "--is-asynchronous",
                "-ia"
            ),
            "kwargs": {
                "dest": "is_asynchronous",
                "help": "Is asynchronous.",
                "required": False,
                "default": False,
                "type": bool,
            }
        },
        {
            "args": (
                "--is-cli-output-hidden",
                "-icoh"
            ),
            "kwargs": {
                "dest": "is_cli_output_hidden",
                "help": "Is CLI output hidden.",
                "required": False,
                "default": False,
                "type": bool,
            }
        },
        {
            "args": (
                "--cli-result-filesystem-paths",
                "-cofp"
            ),
            "kwargs": {
                "dest": "cli_result_filesystem_paths",
                "help": "CLI result filesystem paths.",
                "required": False,
                "default": (),
                "type": str,
                "nargs": "+",
            }
        },
    )

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
                                    "name": "filesystem",
                                    "args": (),
                                    "kwargs": { "help": "Manage filesystem operations.", },
                                    "subcommands": [
                                        {
                                            "name": "create",
                                            "kwargs": { "help": "Create filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_create_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-paths",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_paths",
                                                        "help": "Existing or non-existing filesystem paths.",
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
                                            "kwargs": { "help": "Remove filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_remove_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-paths",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_paths",
                                                        "help": "Existing or non-existing filesystem paths.",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--target_regex-patterns",
                                                        "-trp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "move",
                                            "kwargs": { "help": "Move filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_move_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--input-filesystem-path",
                                                        "-ifp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_filesystem_path",
                                                        "help": "Input filesystem path.",
                                                        "required": True,
                                                        "type": str,
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--output-filesystem-path",
                                                        "-ofp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "output_filesystem_path",
                                                        "help": "Output filesystem path.",
                                                        "required": True,
                                                        "type": str,
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--input-regex-patterns",
                                                        "-irp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "copy",
                                            "kwargs": { "help": "Copy filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_copy_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--input-filesystem-paths",
                                                        "-ifp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_filesystem_paths",
                                                        "help": "Input filesystem paths",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--output-filesystem-paths",
                                                        "-ofp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "output_filesystem_paths",
                                                        "help": "Output filesystem paths",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--input-regex-patterns",
                                                        "-irp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "compress",
                                            "kwargs": { "help": "Compress filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_compress_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--input-filesystem-paths",
                                                        "-ifp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_filesystem_paths",
                                                        "help": "Input filesystem paths.",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },                                                
                                                {
                                                    "args": (
                                                        "--output-filesystem-paths",
                                                        "-ofp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "output_filesystem_paths",
                                                        "help": "Output filesystem paths.",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },                                                
                                                {
                                                    "args": (
                                                        "--excluded-filesystem-paths",
                                                        "-efp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "excluded_filesystem_paths",
                                                        "help": "Excluded filesystem paths.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--input-regex-patterns",
                                                        "-irp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "input_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--excluded-regex-patterns",
                                                        "-erp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "excluded_regex_patterns",
                                                        "help": "Python3 regex patterns for excluding filesystem sub entities.",
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
                                                        "help": "Compression format.",
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
                                                        "help": "Compression type.",
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
                                                        "help": "Compression level.",
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
                                                        "help": "Zip 64 option.",
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
                                                        "help": "Timestamp strictness option.",
                                                        "required": False,
                                                        "default": True,
                                                        "type": bool,
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "size",
                                            "kwargs": { "help": "Show filesystem size.", },
                                            "command_handler": (
                                                run_filesystem_size_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-path",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_path",
                                                        "help": "Target filesystem path.",
                                                        "required": True,
                                                        "type": str,
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--target-regex-patterns",
                                                        "-trp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "list",
                                            "kwargs": { "help": "Show filesystem paths.", },
                                            "command_handler": (
                                                run_filesystem_list_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-paths",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_paths",
                                                        "help": "Target filesystem paths.",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--target-regex-patterns",
                                                        "-trp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "count",
                                            "kwargs": { "help": "Show filesystem count.", },
                                            "command_handler": (
                                                run_filesystem_count_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-paths",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_paths",
                                                        "help": "Target filesystem paths.",
                                                        "required": True,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--target-regex-patterns",
                                                        "-trp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
                                            ],
                                        },
                                        {
                                            "name": "metadata",
                                            "kwargs": { "help": "Show filesystem metadata.", },
                                            "command_handler": (
                                                run_filesystem_metadata_command
                                            ),
                                            "arguments": [
                                                {
                                                    "args": (
                                                        "--target-filesystem-path",
                                                        "-tfp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_filesystem_path",
                                                        "help": "Target filesystem path.",
                                                        "required": True,
                                                        "type": str,
                                                    }
                                                },
                                                {
                                                    "args": (
                                                        "--target-regex-patterns",
                                                        "-trp"
                                                    ),
                                                    "kwargs": {
                                                        "dest": "target_regex_patterns",
                                                        "help": "Python3 regex patterns for selecting filesystem sub entities.",
                                                        "required": False,
                                                        "default": (),
                                                        "type": str,
                                                        "nargs": "+",
                                                    }
                                                },
                                                *default_cli_options
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
