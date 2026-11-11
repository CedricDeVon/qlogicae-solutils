from __future__ import annotations

from typing import Any

_PluginManager: Any = None
_DatabaseManager: Any = None
_DependencyManager: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _PluginManager
    global _DatabaseManager
    global _DependencyManager

    from qlogicae_solutils.library import (
        database_manager,
        dependency_manager,
        plugin_manager,
    )

    _PluginManager = (
        plugin_manager
            .PluginManager
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


class ConsoleManager:
    _singleton: Any = None

    def __init__(self) -> None:
        _handle_dynamic_imports()

        self._console_parser: Any = None
        self._console_commands: Any = None
        self._console_arguments: Any = None
        self._plugin_modules: tuple[Any, ...] = tuple()

    @classmethod
    def singleton(cls) -> Any:
        if not cls._singleton:
            cls._singleton = ConsoleManager()

        return (
            cls._singleton
        )

    def run(self) -> int:
        try:
            result_value: bool = True
            result_value = (
                self.setup_plugin_modules() and result_value
            )
            result_value = (
                self.setup_console_commands() and result_value
            )
            result_value = (
                self.setup_parsed_console_arguments() and result_value
            )

            command_handler = getattr(
                self._console_arguments,
                "command_handler",
                None,
            )

            if command_handler is not None:
                result_value = command_handler(
                    self._console_arguments
                ) and result_value

            else:
                self._console_parser.print_help()

            return 0 if result_value else 1

        except (OSError, ValueError, RuntimeError) as error:
            print(f"{error}")

            return 1

    def setup_plugin_modules(self) -> bool:
        plugin_manager: Any = (
            _PluginManager
                .singleton()
        )

        plugin_modules: tuple[Any, ...] = (
            plugin_manager
                .read_plugin_modules()
        )

        self._plugin_modules = (
            plugin_modules
        )

        return True

    def setup_console_commands(self) -> bool:
        dependency_manager: Any = _DependencyManager.singleton()
        database_manager: Any = _DatabaseManager.singleton()

        console: Any = (
            dependency_manager
                .setup_console_parser(
                    keyword_properties={
                        "prog": (
                            database_manager
                                .read_base_console_command_name()
                        ),
                        "description": (
                            database_manager
                                .read_inner_configuration_project_description()
                        ),
                    }
                )
        )
        console_commands: Any = (
            dependency_manager
                .setup_console_command_parser(
                    console=console,
                    keyword_properties={
                        "dest": "command_handler",
                        "metavar": "",
                    }
                )
        )

        for plugin_module in self._plugin_modules:
            if not plugin_module:
                continue

            plugin_module_exports: Any = (
                getattr(
                    plugin_module,
                    "exports",
                    {}
                )
            )
            if not plugin_module_exports:
                continue

            plugin_module_export_commands: tuple[Any, ...] = (
                plugin_module_exports.get(
                    "commands",
                    tuple()
                ) or tuple()
            )
            if not plugin_module_export_commands:
                continue

            for export_command in plugin_module_export_commands:
                if not export_command:
                    continue

                export_command_setup: Any = (
                    export_command.get(
                        "setup",
                        None
                    ) or None
                )

                if not export_command_setup:
                    continue

                export_command_setup(
                    console=console_commands
                )

        self._console_parser = (
            console
        )
        self.console_commands = (
            console_commands
        )

        return True

    def setup_parsed_console_arguments(self) -> bool:
        arguments = self._console_parser.parse_args()

        self._console_arguments = (
            arguments
        )

        return True



# separate dynamic import allocation /
# json configurations ???
# disk cache ???
# public and private configurations ???
