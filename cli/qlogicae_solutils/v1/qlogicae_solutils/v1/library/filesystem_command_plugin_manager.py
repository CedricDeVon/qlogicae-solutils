__all__ = (
    "FilesystemCommandPluginManager",
)

_FilesystemCommandPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FilesystemCommandPluginManager

    class __FilesystemCommandPluginManager:
        __slots__ = (
            "_plugin_exports",
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

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

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
                                            "name": "filesystem",
                                            "args": (),
                                            "kwargs": { "help": "Manage filesystem operations.", },
                                            "subcommands": [
                                                {
                                                    "name": "create",
                                                    "kwargs": { "help": "Create filesystem paths.", },
                                                    "subcommands": [
                                                        {
                                                            "name": "file",
                                                            "args": (),
                                                            "kwargs": { "help": "Create files.", },
                                                            "command_handler": (
                                                                self.run_filesystem_create_file_command
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
                                                                        "--content",
                                                                        "-c"
                                                                    ),
                                                                    "kwargs": {
                                                                        "dest": "content",
                                                                        "help": "File content.",
                                                                        "required": False,
                                                                        "default": "",
                                                                        "type": str,
                                                                    }
                                                                },
                                                                {
                                                                    "args": (
                                                                        "--encoding",
                                                                        "-e"
                                                                    ),
                                                                    "kwargs": {
                                                                        "dest": "encoding",
                                                                        "help": "File encoding.",
                                                                        "required": False,
                                                                        "default": "utf-8",
                                                                        "type": str,
                                                                    }
                                                                },
                                                                {
                                                                    "args": (
                                                                        "--is-overwrite-enabled",
                                                                        "-ioe"
                                                                    ),
                                                                    "kwargs": {
                                                                        "dest": "is_overwrite_enabled",
                                                                        "help": "Is content overwrite enabled.",
                                                                        "required": False,
                                                                        "default": False,
                                                                        "type": bool,
                                                                    }
                                                                },
                                                                *default_cli_options
                                                            ],
                                                        },
                                                        {
                                                            "name": "folder",
                                                            "args": (),
                                                            "kwargs": { "help": "Create folders.", },
                                                            "command_handler": (
                                                                self.run_filesystem_create_folder_command
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
                                                                *default_cli_options                                             
                                                            ],
                                                        },
                                                    ],
                                                },
                                                {
                                                    "name": "remove",
                                                    "kwargs": { "help": "Remove filesystem paths.", },
                                                    "command_handler": (
                                                        self.run_filesystem_remove_command
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
                                                        {
                                                            "args": (
                                                                "--excluded-filesystem-paths",
                                                                "-efp"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "excluded_filesystem_paths",
                                                                "help": "Existing or non-existing filesystem paths.",
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
                                                                "help": "Python3 regex patterns for unselecting filesystem sub entities.",
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
                                                        self.run_filesystem_move_command
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
                                                        self.run_filesystem_copy_command
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
                                                        self.run_filesystem_compress_command
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
                                                    "name": "list",
                                                    "kwargs": { "help": "Show filesystem paths.", },
                                                    "command_handler": (
                                                        self.run_filesystem_list_command
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
                                                        self.run_filesystem_count_command
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
                                                    "name": "size",
                                                    "kwargs": { "help": "Show filesystem size.", },
                                                    "command_handler": (
                                                        self.run_filesystem_size_command
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
                                                                "--unit",
                                                                "-u"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "unit",
                                                                "help": "Filesystem size unit of measurement.",
                                                                "required": False,
                                                                "default": "B",
                                                                "type": str,
                                                                "choices": (
                                                                    "b", "bit", "bits",
                                                                    "B", "byte", "bytes",
                                                                    "kb", "kilobit", "kilobits",
                                                                    "kB", "kilobyte", "kilobytes",
                                                                    "Mb", "megabit", "megabits",
                                                                    "MB", "megabyte", "megabytes",
                                                                    "Gb", "gigabit", "gigabits",
                                                                    "GB", "gigabyte", "gigabytes",
                                                                    "Tb", "terabit", "terabits",
                                                                    "TB", "terabyte", "terabytes",
                                                                    "Pb", "petabit", "petabits",
                                                                    "PB", "petabyte", "petabytes",
                                                                    "Kib", "kibibit", "kibibits",
                                                                    "KiB", "kibibyte", "kibibytes",
                                                                    "Mib", "mebibit", "mebibits",
                                                                    "MiB", "mebibyte", "mebibytes",
                                                                    "Gib", "gibibit", "gibibits",
                                                                    "GiB", "gibibyte", "gibibytes",
                                                                    "Tib", "tebibit", "tebibits",
                                                                    "TiB", "tebibyte", "tebibytes",
                                                                    "Pib", "pebibit", "pebibits",
                                                                    "PiB", "pebibyte", "pebibytes",
                                                                ),
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
                                                        self.run_filesystem_metadata_command
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
                                                        {
                                                            "args": (
                                                                "--properties",
                                                                "-p"
                                                            ),
                                                            "kwargs": {
                                                                "dest": "properties",
                                                                "help": "Properties.",
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

            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)) or not kwargs:
                raise ValueError("'kwargs' must be a non-empty dictionary")

            return True

        def shutdown(self):
            return True                

        def run_filesystem_create_file_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path

            if not arguments:
                raise ValueError("'arguments' must be defined")

            if isinstance(arguments, dict):
                target_filesystem_paths = arguments.get(
                    "target_filesystem_paths"
                )
                content = arguments.get("content", "")
                is_overwrite_enabled = arguments.get(
                    "is_overwrite_enabled",
                    False
                )
                encoding = arguments.get(
                    "encoding",
                    "utf-8"
                )
            else:
                target_filesystem_paths = getattr(
                    arguments,
                    "target_filesystem_paths",
                    None
                )
                content = getattr(arguments, "content", "")
                is_overwrite_enabled = getattr(
                    arguments,
                    "is_overwrite_enabled",
                    False
                )
                encoding = getattr(
                    arguments,
                    "encoding",
                    "utf-8"
                )

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if not isinstance(content, str):
                raise TypeError("'content' must be a string")

            if not isinstance(is_overwrite_enabled, bool):
                raise TypeError("'is_overwrite_enabled' must be a boolean")

            try:
                for target_filesystem_path in target_filesystem_paths:
                    path = Path(target_filesystem_path)

                    path.parent.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    if path.exists() and not is_overwrite_enabled:
                        continue

                    path.write_text(
                        content,
                        encoding=encoding
                    )

            except (OSError, ValueError, TypeError):
                return False

            return True

        def run_filesystem_create_folder_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path

            if isinstance(arguments, dict):
                target_filesystem_paths = arguments.get(
                    "target_filesystem_paths"
                )
            else:
                target_filesystem_paths = getattr(
                    arguments,
                    "target_filesystem_paths",
                    None
                )

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            try:
                for target_filesystem_path in target_filesystem_paths:
                    Path(target_filesystem_path).mkdir(
                        parents=True,
                        exist_ok=True
                    )
            except (OSError, ValueError, TypeError):
                return False

            return True

        def run_filesystem_remove_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import os
            import re

            get_argument = (
                arguments.get
                if isinstance(arguments, dict)
                else lambda name, default=None: getattr(arguments, name, default)
            )

            target_filesystem_paths = get_argument("target_filesystem_paths", ())
            target_regex_patterns = get_argument("target_regex_patterns", ())
            excluded_filesystem_paths = get_argument("excluded_filesystem_paths", ())
            excluded_regex_patterns = get_argument("excluded_regex_patterns", ())

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            def normalize(value):
                if isinstance(value, (str, Path)):
                    return (value,)
                return tuple(value)

            target_filesystem_paths = normalize(target_filesystem_paths)
            target_regex_patterns = normalize(target_regex_patterns)
            excluded_filesystem_paths = normalize(excluded_filesystem_paths)
            excluded_regex_patterns = normalize(excluded_regex_patterns)

            try:
                target_patterns = tuple(re.compile(pattern) for pattern in target_regex_patterns)
                excluded_patterns = tuple(re.compile(pattern) for pattern in excluded_regex_patterns)

                def absolute_path(value):
                    return Path(os.path.abspath(os.fspath(value)))

                current_path = absolute_path(Path.cwd())
                excluded_paths = {
                    current_path,
                    *(absolute_path(path) for path in excluded_filesystem_paths),
                }

                def is_within(path, parent):
                    return path == parent or path.is_relative_to(parent)

                def is_excluded(path, root):
                    if any(is_within(path, excluded) for excluded in excluded_paths):
                        return True

                    if any(is_within(excluded, path) for excluded in excluded_paths):
                        return True

                    relative_path = path.relative_to(root).as_posix()

                    return any(
                        pattern.search(relative_path)
                        for pattern in excluded_patterns
                    )

                def remove_path(path, root, inherited_selection=False):
                    if is_excluded(path, root):
                        return False

                    relative_path = path.relative_to(root).as_posix()

                    is_selected = (
                        inherited_selection
                        or not target_patterns
                        or any(pattern.search(relative_path) for pattern in target_patterns)
                    )

                    if path.is_symlink() or not path.is_dir():
                        if is_selected:
                            path.unlink()
                            return True
                        return False

                    is_modified = False

                    for child in path.iterdir():
                        if remove_path(child, root, is_selected):
                            is_modified = True

                    if is_selected or is_modified:
                        try:
                            path.rmdir()
                            return True
                        except OSError:
                            pass

                    return is_modified

                for target in target_filesystem_paths:
                    root = absolute_path(target)

                    if not root.exists() and not root.is_symlink():
                        continue

                    if any(is_within(root, excluded) for excluded in excluded_paths):
                        continue

                    if any(is_within(excluded, root) for excluded in excluded_paths):
                        if root.is_dir() and not root.is_symlink():
                            for child in root.iterdir():
                                remove_path(child, root, False)
                            continue
                        continue

                    remove_path(root, root)

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_move_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import os
            import re
            import shutil

            get_argument = (
                arguments.get
                if isinstance(arguments, dict)
                else lambda name, default=None: getattr(arguments, name, default)
            )

            input_filesystem_path = get_argument("input_filesystem_path")
            output_filesystem_path = get_argument("output_filesystem_path")
            input_regex_patterns = get_argument("input_regex_patterns", ())

            if not input_filesystem_path:
                raise ValueError("'input_filesystem_path' must be defined")

            if not output_filesystem_path:
                raise ValueError("'output_filesystem_path' must be defined")

            if isinstance(input_regex_patterns, str):
                input_regex_patterns = (input_regex_patterns,)

            try:
                source = Path(os.path.abspath(os.fspath(input_filesystem_path)))
                destination = Path(os.path.abspath(os.fspath(output_filesystem_path)))

                if not source.exists() and not source.is_symlink():
                    return False

                if source == destination:
                    return False

                patterns = tuple(re.compile(pattern) for pattern in input_regex_patterns)

                if not patterns:
                    if source.is_dir() and not source.is_symlink():
                        if destination.is_relative_to(source):
                            return False

                    if destination.exists() or destination.is_symlink():
                        return False

                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(destination))
                    return True

                if not source.is_dir() or source.is_symlink():
                    return False

                if destination.is_relative_to(source):
                    return False

                if destination.exists() and not destination.is_dir():
                    return False

                selected_paths = []

                for path in source.rglob("*"):
                    relative_path = path.relative_to(source).as_posix()

                    if any(pattern.search(relative_path) for pattern in patterns):
                        selected_paths.append(path)

                selected_paths.sort(key=lambda path: (len(path.parts), path.as_posix()))

                filtered_paths = []

                for path in selected_paths:
                    if any(path.is_relative_to(parent) for parent in filtered_paths):
                        continue
                    filtered_paths.append(path)

                operations = []

                for path in filtered_paths:
                    relative_path = path.relative_to(source)
                    target = destination / relative_path

                    if target.exists() or target.is_symlink():
                        return False

                    operations.append((path, target))

                for path, target in operations:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), str(target))

                for path in sorted(
                    source.rglob("*"),
                    key=lambda item: len(item.parts),
                    reverse=True,
                ):
                    if path.is_dir() and not path.is_symlink():
                        try:
                            path.rmdir()
                        except OSError:
                            pass

                try:
                    source.rmdir()
                except OSError:
                    pass

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_copy_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import os
            import re
            import shutil

            get_argument = (
                arguments.get
                if isinstance(arguments, dict)
                else lambda name, default=None: getattr(arguments, name, default)
            )

            input_filesystem_paths = get_argument("input_filesystem_paths", ())
            output_filesystem_paths = get_argument("output_filesystem_paths", ())
            input_regex_patterns = get_argument("input_regex_patterns", ())

            if not input_filesystem_paths:
                raise ValueError("'input_filesystem_paths' must be defined")

            if not output_filesystem_paths:
                raise ValueError("'output_filesystem_paths' must be defined")

            def normalize(value):
                if isinstance(value, (str, Path)):
                    return (value,)
                return tuple(value)

            input_filesystem_paths = normalize(input_filesystem_paths)
            output_filesystem_paths = normalize(output_filesystem_paths)
            input_regex_patterns = normalize(input_regex_patterns)

            if len(input_filesystem_paths) != len(output_filesystem_paths):
                raise ValueError(
                    "'input_filesystem_paths' and 'output_filesystem_paths' "
                    "must contain the same number of paths"
                )

            try:
                patterns = tuple(re.compile(pattern) for pattern in input_regex_patterns)

                def copy_item(source, destination):
                    if destination.exists() or destination.is_symlink():
                        raise FileExistsError(str(destination))

                    destination.parent.mkdir(parents=True, exist_ok=True)

                    if source.is_symlink():
                        os.symlink(os.readlink(source), destination)
                    elif source.is_dir():
                        shutil.copytree(source, destination, symlinks=True)
                    else:
                        shutil.copy2(source, destination, follow_symlinks=False)

                operations = []

                for input_path, output_path in zip(
                    input_filesystem_paths,
                    output_filesystem_paths,
                ):
                    source = Path(os.path.abspath(os.fspath(input_path)))
                    destination = Path(os.path.abspath(os.fspath(output_path)))

                    if not source.exists() and not source.is_symlink():
                        return False

                    if source == destination:
                        return False

                    if source.is_dir() and not source.is_symlink():
                        if destination.is_relative_to(source):
                            return False

                        if source.is_relative_to(destination):
                            return False

                        if not patterns:
                            operations.append((source, destination, True))
                            continue

                        selected_paths = []

                        for path in source.rglob("*"):
                            relative_path = path.relative_to(source).as_posix()

                            if any(pattern.search(relative_path) for pattern in patterns):
                                selected_paths.append(path)

                        selected_paths.sort(
                            key=lambda path: (len(path.parts), path.as_posix())
                        )

                        filtered_paths = []

                        for path in selected_paths:
                            if any(path.is_relative_to(parent) for parent in filtered_paths):
                                continue
                            filtered_paths.append(path)

                        for path in filtered_paths:
                            target = destination / path.relative_to(source)
                            operations.append((path, target, path.is_dir() and not path.is_symlink()))

                    else:
                        if patterns:
                            return False

                        operations.append((source, destination, False))

                for source, destination, is_directory in operations:
                    if destination.exists() or destination.is_symlink():
                        return False

                    if is_directory:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(source, destination, symlinks=True)
                    else:
                        copy_item(source, destination)

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_compress_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import os
            import re
            import tempfile
            import zipfile

            get_argument = (
                arguments.get
                if isinstance(arguments, dict)
                else lambda name, default=None: getattr(arguments, name, default)
            )

            input_filesystem_paths = get_argument("input_filesystem_paths", ())
            output_filesystem_paths = get_argument("output_filesystem_paths", ())
            excluded_filesystem_paths = get_argument("excluded_filesystem_paths", ())
            input_regex_patterns = get_argument("input_regex_patterns", ())
            excluded_regex_patterns = get_argument("excluded_regex_patterns", ())
            compression_format = get_argument("format", "zip")
            compression_type = get_argument("type", "deflated")
            compression_level = get_argument("level", 6)
            is_zip_64_allowed = get_argument("is_zip_64_allowed", True)
            is_timestamp_strict = get_argument("is_timestamp_strict", True)

            if not input_filesystem_paths:
                raise ValueError("'input_filesystem_paths' must be defined")

            if not output_filesystem_paths:
                raise ValueError("'output_filesystem_paths' must be defined")

            def normalize(value):
                if isinstance(value, (str, Path)):
                    return (value,)
                return tuple(value)

            input_filesystem_paths = normalize(input_filesystem_paths)
            output_filesystem_paths = normalize(output_filesystem_paths)
            excluded_filesystem_paths = normalize(excluded_filesystem_paths)
            input_regex_patterns = normalize(input_regex_patterns)
            excluded_regex_patterns = normalize(excluded_regex_patterns)

            if len(input_filesystem_paths) != len(output_filesystem_paths):
                raise ValueError(
                    "'input_filesystem_paths' and 'output_filesystem_paths' "
                    "must contain the same number of paths"
                )

            try:
                if not isinstance(compression_format, str):
                    return False

                if compression_format.lower() != "zip":
                    return False

                if not isinstance(compression_type, str):
                    return False

                compression_types = {
                    "stored": zipfile.ZIP_STORED,
                    "deflated": zipfile.ZIP_DEFLATED,
                    "bzip2": zipfile.ZIP_BZIP2,
                    "lzma": zipfile.ZIP_LZMA,
                }

                normalized_type = compression_type.lower()

                if normalized_type not in compression_types:
                    return False

                if (
                    not isinstance(compression_level, int)
                    or isinstance(compression_level, bool)
                ):
                    return False

                if not isinstance(is_zip_64_allowed, bool):
                    return False

                if not isinstance(is_timestamp_strict, bool):
                    return False

                input_patterns = tuple(
                    re.compile(pattern) for pattern in input_regex_patterns
                )
                excluded_patterns = tuple(
                    re.compile(pattern) for pattern in excluded_regex_patterns
                )

                def absolute_path(value):
                    return Path(os.path.abspath(os.fspath(value)))

                def is_within(path, parent):
                    return path == parent or path.is_relative_to(parent)

                current_path = absolute_path(Path.cwd())
                excluded_paths = {
                    current_path,
                    *(absolute_path(path) for path in excluded_filesystem_paths),
                }

                compression_method = compression_types[normalized_type]
                operations = []

                for input_path, output_path in zip(
                    input_filesystem_paths,
                    output_filesystem_paths,
                ):
                    source = absolute_path(input_path)
                    destination = absolute_path(output_path)

                    if not source.exists() and not source.is_symlink():
                        return False

                    if source.is_symlink():
                        return False

                    if not source.is_file() and not source.is_dir():
                        return False

                    if destination.exists() or destination.is_symlink():
                        return False

                    if source == destination:
                        return False

                    if source.is_dir() and is_within(destination, source):
                        return False

                    if any(is_within(source, excluded) for excluded in excluded_paths):
                        return False

                    selected_files = []

                    if source.is_dir():
                        for path in source.rglob("*"):
                            if path.is_symlink() or not path.is_file():
                                continue

                            absolute_file_path = absolute_path(path)

                            if any(
                                is_within(absolute_file_path, excluded)
                                for excluded in excluded_paths
                            ):
                                continue

                            relative_path = path.relative_to(source).as_posix()

                            if input_patterns and not any(
                                pattern.search(relative_path)
                                for pattern in input_patterns
                            ):
                                continue

                            if any(
                                pattern.search(relative_path)
                                for pattern in excluded_patterns
                            ):
                                continue

                            selected_files.append((path, relative_path))

                    else:
                        relative_path = source.name

                        if input_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in input_patterns
                        ):
                            continue

                        if any(
                            pattern.search(relative_path)
                            for pattern in excluded_patterns
                        ):
                            continue

                        selected_files.append((source, relative_path))

                    operations.append((destination, selected_files))

                for destination, selected_files in operations:
                    destination.parent.mkdir(parents=True, exist_ok=True)

                    temporary_path = None

                    try:
                        with tempfile.NamedTemporaryFile(
                            dir=destination.parent,
                            prefix=f".{destination.name}.",
                            suffix=".tmp",
                            delete=False,
                        ) as temporary_file:
                            temporary_path = Path(temporary_file.name)

                        with zipfile.ZipFile(
                            temporary_path,
                            mode="w",
                            compression=compression_method,
                            compresslevel=(
                                compression_level
                                if compression_method in (
                                    zipfile.ZIP_DEFLATED,
                                    zipfile.ZIP_BZIP2,
                                    zipfile.ZIP_LZMA,
                                )
                                else None
                            ),
                            allowZip64=is_zip_64_allowed,
                            strict_timestamps=is_timestamp_strict,
                        ) as archive:
                            for source, archive_name in selected_files:
                                archive.write(source, arcname=archive_name)

                        if destination.exists() or destination.is_symlink():
                            return False

                        os.replace(temporary_path, destination)
                        temporary_path = None

                    finally:
                        if temporary_path is not None:
                            try:
                                temporary_path.unlink()
                            except OSError:
                                pass

                return True

            except (
                OSError,
                ValueError,
                TypeError,
                RuntimeError,
                re.error,
                zipfile.BadZipFile,
            ):
                return False

        def run_filesystem_list_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import re

            if not arguments:
                raise ValueError("'arguments' must be defined")

            if isinstance(arguments, dict):
                get_argument = arguments.get
            else:
                get_argument = lambda name, default=None: getattr(
                    arguments,
                    name,
                    default
                )

            target_filesystem_paths = get_argument(
                "target_filesystem_paths",
                ()
            )
            target_regex_patterns = get_argument(
                "target_regex_patterns",
                ()
            )

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            try:
                compiled_patterns = tuple(
                    re.compile(pattern)
                    for pattern in target_regex_patterns
                )

                for target_filesystem_path in target_filesystem_paths:
                    root = Path(target_filesystem_path)

                    if not root.exists() and not root.is_symlink():
                        continue

                    if root.is_file() or root.is_symlink():
                        if not compiled_patterns or any(
                            pattern.search(root.name)
                            for pattern in compiled_patterns
                        ):
                            print(root)
                        continue

                    for path in sorted(root.rglob("*")):
                        relative_path = path.relative_to(root).as_posix()

                        if compiled_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in compiled_patterns
                        ):
                            continue

                        print(path)

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_count_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import re

            if not arguments:
                raise ValueError("'arguments' must be defined")

            if isinstance(arguments, dict):
                get_argument = arguments.get
            else:
                get_argument = lambda name, default=None: getattr(
                    arguments,
                    name,
                    default
                )

            target_filesystem_paths = get_argument(
                "target_filesystem_paths",
                ()
            )
            target_regex_patterns = get_argument(
                "target_regex_patterns",
                ()
            )

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            try:
                compiled_patterns = tuple(
                    re.compile(pattern)
                    for pattern in target_regex_patterns
                )

                total_count = 0

                for target_filesystem_path in target_filesystem_paths:
                    root = Path(target_filesystem_path)

                    if not root.exists() and not root.is_symlink():
                        continue

                    if root.is_file() or root.is_symlink():
                        if not compiled_patterns or any(
                            pattern.search(root.name)
                            for pattern in compiled_patterns
                        ):
                            total_count += 1

                        continue

                    for path in root.rglob("*"):
                        relative_path = path.relative_to(root).as_posix()

                        if compiled_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in compiled_patterns
                        ):
                            continue

                        total_count += 1

                print(total_count)

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_size_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            import re

            if not arguments:
                raise ValueError("'arguments' must be defined")

            if isinstance(arguments, dict):
                get_argument = arguments.get
            else:
                get_argument = lambda name, default=None: getattr(
                    arguments,
                    name,
                    default
                )

            target_filesystem_paths = get_argument(
                "target_filesystem_paths",
                ()
            )
            target_regex_patterns = get_argument(
                "target_regex_patterns",
                ()
            )
            unit = get_argument("unit", "B")

            if not target_filesystem_paths:
                raise ValueError("'target_filesystem_paths' must be defined")

            if isinstance(target_filesystem_paths, str):
                target_filesystem_paths = (target_filesystem_paths,)

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            units = {
                "b": 1 / 8,
                "bit": 1 / 8,
                "bits": 1 / 8,
                "B": 1,
                "byte": 1,
                "bytes": 1,
                "kb": 1000 / 8,
                "kilobit": 1000 / 8,
                "kilobits": 1000 / 8,
                "kB": 1000,
                "kilobyte": 1000,
                "kilobytes": 1000,
                "Mb": 1000 ** 2 / 8,
                "megabit": 1000 ** 2 / 8,
                "megabits": 1000 ** 2 / 8,
                "MB": 1000 ** 2,
                "megabyte": 1000 ** 2,
                "megabytes": 1000 ** 2,
                "Gb": 1000 ** 3 / 8,
                "gigabit": 1000 ** 3 / 8,
                "gigabits": 1000 ** 3 / 8,
                "GB": 1000 ** 3,
                "gigabyte": 1000 ** 3,
                "gigabytes": 1000 ** 3,
                "Tb": 1000 ** 4 / 8,
                "terabit": 1000 ** 4 / 8,
                "terabits": 1000 ** 4 / 8,
                "TB": 1000 ** 4,
                "terabyte": 1000 ** 4,
                "terabytes": 1000 ** 4,
                "Pb": 1000 ** 5 / 8,
                "petabit": 1000 ** 5 / 8,
                "petabits": 1000 ** 5 / 8,
                "PB": 1000 ** 5,
                "petabyte": 1000 ** 5,
                "petabytes": 1000 ** 5,
                "Kib": 1024 / 8,
                "kibibit": 1024 / 8,
                "kibibits": 1024 / 8,
                "KiB": 1024,
                "kibibyte": 1024,
                "kibibytes": 1024,
                "Mib": 1024 ** 2 / 8,
                "mebibit": 1024 ** 2 / 8,
                "mebibits": 1024 ** 2 / 8,
                "MiB": 1024 ** 2,
                "mebibyte": 1024 ** 2,
                "mebibytes": 1024 ** 2,
                "Gib": 1024 ** 3 / 8,
                "gibibit": 1024 ** 3 / 8,
                "gibibits": 1024 ** 3 / 8,
                "GiB": 1024 ** 3,
                "gibibyte": 1024 ** 3,
                "gibibytes": 1024 ** 3,
                "Tib": 1024 ** 4 / 8,
                "tebibit": 1024 ** 4 / 8,
                "tebibits": 1024 ** 4 / 8,
                "TiB": 1024 ** 4,
                "tebibyte": 1024 ** 4,
                "tebibytes": 1024 ** 4,
                "Pib": 1024 ** 5 / 8,
                "pebibit": 1024 ** 5 / 8,
                "pebibits": 1024 ** 5 / 8,
                "PiB": 1024 ** 5,
                "pebibyte": 1024 ** 5,
                "pebibytes": 1024 ** 5,
            }

            if unit not in units:
                raise ValueError(f"Unsupported filesystem size unit: {unit}")

            try:
                compiled_patterns = tuple(
                    re.compile(pattern)
                    for pattern in target_regex_patterns
                )

                total_size = 0

                for target_filesystem_path in target_filesystem_paths:
                    root = Path(target_filesystem_path)

                    if not root.exists() and not root.is_symlink():
                        continue

                    if root.is_symlink():
                        continue

                    if root.is_file():
                        if not compiled_patterns or any(
                            pattern.search(root.name)
                            for pattern in compiled_patterns
                        ):
                            total_size += root.stat().st_size

                        continue

                    for path in root.rglob("*"):
                        if path.is_symlink() or not path.is_file():
                            continue

                        relative_path = path.relative_to(root).as_posix()

                        if compiled_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in compiled_patterns
                        ):
                            continue

                        total_size += path.stat().st_size

                result = total_size / units[unit]

                print(f"{result:g} {unit}")

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False

        def run_filesystem_metadata_command(self, arguments):
            if not isinstance(arguments, object) or not arguments:
                raise ValueError("'arguments' must be defined")

            from pathlib import Path
            from datetime import datetime, timezone
            import json
            import re
            import stat

            if isinstance(arguments, dict):
                get_argument = arguments.get
            else:
                get_argument = lambda name, default=None: getattr(
                    arguments,
                    name,
                    default
                )

            target_filesystem_path = get_argument(
                "target_filesystem_path"
            )
            target_regex_patterns = get_argument(
                "target_regex_patterns",
                ()
            )
            properties = get_argument(
                "properties",
                ()
            )

            if not target_filesystem_path:
                raise ValueError("'target_filesystem_path' must be defined")

            if isinstance(target_regex_patterns, str):
                target_regex_patterns = (target_regex_patterns,)

            if isinstance(properties, str):
                properties = (properties,)

            property_names = {
                "path",
                "name",
                "type",
                "size",
                "permissions",
                "mode",
                "owner_id",
                "group_id",
                "hard_links",
                "device_id",
                "inode",
                "created_at",
                "changed_at",
                "modified_at",
                "accessed_at",
            }

            if properties:
                invalid_properties = set(properties) - property_names

                if invalid_properties:
                    raise ValueError(
                        f"Unsupported metadata properties: "
                        f"{', '.join(sorted(invalid_properties))}"
                    )

            try:
                root = Path(target_filesystem_path)

                if not root.exists() and not root.is_symlink():
                    return False

                compiled_patterns = tuple(
                    re.compile(pattern)
                    for pattern in target_regex_patterns
                )

                if root.is_file() or root.is_symlink():
                    paths = (root,)
                else:
                    paths = (root, *root.rglob("*"))

                results = []

                for path in paths:
                    if path != root:
                        relative_path = path.relative_to(root).as_posix()

                        if compiled_patterns and not any(
                            pattern.search(relative_path)
                            for pattern in compiled_patterns
                        ):
                            continue

                    metadata = path.lstat()
                    mode = metadata.st_mode

                    if stat.S_ISLNK(mode):
                        filesystem_type = "symlink"
                    elif stat.S_ISDIR(mode):
                        filesystem_type = "directory"
                    elif stat.S_ISREG(mode):
                        filesystem_type = "file"
                    elif stat.S_ISFIFO(mode):
                        filesystem_type = "fifo"
                    elif stat.S_ISSOCK(mode):
                        filesystem_type = "socket"
                    elif stat.S_ISCHR(mode):
                        filesystem_type = "character_device"
                    elif stat.S_ISBLK(mode):
                        filesystem_type = "block_device"
                    else:
                        filesystem_type = "unknown"

                    created_timestamp = getattr(
                        metadata,
                        "st_birthtime",
                        None
                    )

                    if created_timestamp is None:
                        created_timestamp = getattr(
                            metadata,
                            "st_ctime",
                            None
                        )

                    entry = {
                        "path": str(path),
                        "name": path.name,
                        "type": filesystem_type,
                        "size": metadata.st_size,
                        "permissions": stat.filemode(mode),
                        "mode": oct(mode),
                        "owner_id": getattr(metadata, "st_uid", None),
                        "group_id": getattr(metadata, "st_gid", None),
                        "hard_links": getattr(metadata, "st_nlink", None),
                        "device_id": getattr(metadata, "st_dev", None),
                        "inode": getattr(metadata, "st_ino", None),
                        "created_at": (
                            datetime.fromtimestamp(
                                created_timestamp,
                                tz=timezone.utc
                            ).isoformat()
                            if created_timestamp is not None
                            else None
                        ),
                        "changed_at": (
                            datetime.fromtimestamp(
                                metadata.st_ctime,
                                tz=timezone.utc
                            ).isoformat()
                            if created_timestamp is None
                            and hasattr(metadata, "st_ctime")
                            else None
                        ),
                        "modified_at": datetime.fromtimestamp(
                            metadata.st_mtime,
                            tz=timezone.utc
                        ).isoformat(),
                        "accessed_at": datetime.fromtimestamp(
                            metadata.st_atime,
                            tz=timezone.utc
                        ).isoformat(),
                    }

                    if properties:
                        entry = {
                            property_name: entry[property_name]
                            for property_name in properties
                        }

                    results.append(entry)

                print(
                    json.dumps(
                        results,
                        indent=4,
                        ensure_ascii=False
                    )
                )

                return True

            except (OSError, ValueError, TypeError, re.error):
                return False


    _FilesystemCommandPluginManager = __FilesystemCommandPluginManager
    _allocate = lambda: None


def FilesystemCommandPluginManager():
    if _FilesystemCommandPluginManager is None:
        _allocate()

    return _FilesystemCommandPluginManager

