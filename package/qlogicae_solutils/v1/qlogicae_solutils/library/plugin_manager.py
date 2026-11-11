from __future__ import annotations

from typing import Any

_DatabaseManager: Any = None
_DependencyManager: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _DatabaseManager
    global _DependencyManager

    from qlogicae_solutils.library import (
        database_manager,
        dependency_manager,
    )

    _DependencyManager = (
        dependency_manager
            .DependencyManager
    )
    _DatabaseManager = (
        database_manager
            .DatabaseManager
    )

    _handle_dynamic_imports = lambda: None


class PluginManager:
    _singleton: Any = None

    def __init__(self) -> None:
        _handle_dynamic_imports()

    @classmethod
    def singleton(cls) -> Any:
        if not cls._singleton:
            cls._singleton = PluginManager()

        return (
            cls._singleton
        )

    def read_plugin_modules(self) -> tuple[Any, ...]:
        inner_plugin_modules: tuple[Any, ...] = (
            self.read_inner_plugin_modules()
        )
        outer_plugin_modules: tuple[Any, ...] = (
            self.read_outer_plugin_modules()
        )

        output: tuple[Any, ...] = (
            *inner_plugin_modules,
            *outer_plugin_modules,
        )

        return (
            output
        )

    def read_inner_plugin_modules(self) -> tuple[Any, ...]:
        dependency_manager: Any = (
            _DependencyManager
                .singleton()
        )
        database_manager: Any = (
            _DatabaseManager
                .singleton()
        )

        inner_plugin_modules: tuple[Any, ...] = (
            dependency_manager.import_modules(
                target_filesystem_path=(
                    database_manager
                        .read_inner_plugin_folder_path()
                )
            )
        )

        return (
            inner_plugin_modules
        )

    def read_outer_plugin_modules(self) -> tuple[Any, ...]:
        dependency_manager: Any = (
            _DependencyManager
                .singleton()
        )
        database_manager: Any = (
            _DatabaseManager
                .singleton()
        )

        outer_plugin_modules: tuple[Any, ...] = (
            dependency_manager.import_modules(
                target_filesystem_path=(
                    database_manager
                        .read_outer_plugin_folder_path()
                )
            )
        )

        return (
            outer_plugin_modules
        )

    def setup_export_object(self, **kwargs: Any) -> dict[str, dict[str, Any]]:
        if not kwargs:
            return {}

        commands: tuple[Any, ...] = (kwargs.get("commands", tuple()) or tuple())

        exports: dict[str, Any] = {
            "commands": commands
        }

        return exports
