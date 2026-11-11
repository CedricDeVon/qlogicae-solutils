from __future__ import annotations

from typing import Any

__all__ = (
    "exports"
)

_PluginManager: Any = None
_DependencyManager: Any = None


def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _DependencyManager
    global _PluginManager

    from qlogicae_solutils.library import (
        dependency_manager,
        plugin_manager,
    )

    _DependencyManager = (
        dependency_manager
            .DependencyManager
    )
    _PluginManager = (
        plugin_manager
            .PluginManager
    )
    _handle_dynamic_imports = lambda: None


def _run(arguments: Any) -> bool:
    if not arguments:
        return False

    return True


def _setup(**kwargs: Any) -> bool:
    if not kwargs:
        return False

    console: Any = (kwargs.get("console", {}) or {})

    if not console:
        return False

    dependency_manager: Any = (
        _DependencyManager
            .singleton()
    )

    console_command: Any = (
        dependency_manager.setup_console_sub_command_parser(
            console=console,
            list_properties=(
                "remove-filesystem",
            ),
            keyword_properties={
                "help": "remove filesystem paths"
            }
        )
    )

    dependency_manager.setup_console_command_argument(
        console=console_command,
        list_properties=(
            "--target-paths",
            "-tp",
        ),
        keyword_properties={
            "dest": "target_paths",
            "help": "target filesystem paths",
            "nargs": "+",
            "type": dependency_manager.read_filesystem_path_type(),
            "default": tuple(),
            "required": True,
        }
    )

    dependency_manager.setup_console_command_argument(
        console=console_command,
        list_properties=(
            "--is-atmoic",
            "-ia",
        ),
        keyword_properties={
            "dest": "is_atmoic",
            "type": bool,
            "help": "continue executing after failed execution",
            "default": True,
        }
    )

    dependency_manager.setup_console_command_method_handler(
        console=console_command,
        keyword_properties={
            "command_handler": _run,
        }
    )

    return True


def _export() -> Any:
    _handle_dynamic_imports()

    return (
        _PluginManager
            .singleton()
            .setup_export_object(
                commands=[
                    {
                        "setup": _setup
                    }
                ]
            )
    )

exports = (
    _export()
)
