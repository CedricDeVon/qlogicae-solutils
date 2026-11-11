from __future__ import annotations

from typing import Any

_DependencyManager: Any = None
_project_configuration_utility: Any = None

def _handle_dynamic_imports() -> None:
    global _handle_dynamic_imports
    global _DependencyManager
    global _project_configuration_utility

    from qlogicae_solutils.configuration import utility
    from qlogicae_solutils.library import dependency_manager

    _DependencyManager = dependency_manager.DependencyManager
    _project_configuration_utility = utility

    _handle_dynamic_imports = lambda: None


class DatabaseManager:
    _singleton: Any = None

    def __init__(self) -> None:
        _handle_dynamic_imports()

    @classmethod
    def singleton(cls) -> Any:
        if not cls._singleton:
            cls._singleton = DatabaseManager()

        return (
            cls._singleton
        )

    def read_base_console_command_name(self) -> str:
        value: str = (
            f"{self.read_inner_configuration_company_name()}"
            f"-{self.read_inner_configuration_project_name()}"
        )

        return (
            value
        )

    def read_inner_configuration_company_name(self) -> str:
        value: str = (
            (((getattr(
                _project_configuration_utility,
                "exports",
                {}
            ) or {}).get(
                "data",
                {}
            ) or {}).get(
                "company-name",
                {}
            ) or {}).get(
                "value",
                ""
            ) or ""
        )

        return (
            value
        )

    def read_inner_configuration_project_name(self) -> str:
        value: str = (
            (((getattr(
                _project_configuration_utility,
                "exports",
                {}
            ) or {}).get(
                "data",
                {}
            ) or {}).get(
                "project-name",
                {}
            ) or {}).get(
                "value",
                ""
            ) or ""
        )

        return (
            value
        )

    def read_inner_configuration_project_description(self) -> str:
        value: str = (
            (((getattr(
                _project_configuration_utility,
                "exports",
                {}
            ) or {}).get(
                "data",
                {}
            ) or {}).get(
                "project-description",
                {}
            ) or {}).get(
                "value",
                ""
            ) or ""
        )

        return (
            value
        )

    # def read_inner_configuration_active_major_version_label(self) -> str:
    #     value: str = (
    #         (((getattr(
    #             _project_configuration_utility,
    #             "exports",
    #             {}
    #         ) or {}).get(
    #             "data",
    #             {}
    #         ) or {}).get(
    #             "active-major-version-label",
    #             {}
    #         ) or {}).get(
    #             "value",
    #             ""
    #         ) or ""
    #     )

    #     return (
    #         value
    #     )

    def read_inner_plugin_folder_path(self) -> str:
        dependency_manager: _DependencyManager = (
            _DependencyManager.singleton()
        )

        filesystem_path: str = (
            dependency_manager
                .read_entry_script_folder_path()
        )

        output: str = (
            dependency_manager
                .convert_filesystem_path(
                    targets=(
                        filesystem_path,
                        "qlogicae_solutils",
                        "plugin",
                    )
                )
        )

        return (
            output
        )

    def read_outer_plugin_folder_path(self) -> str:
        dependency_manager: _DependencyManager = (
            _DependencyManager.singleton()
        )

        filesystem_path: str = (
            dependency_manager
                .read_working_console_filesystem_path()
        )

        output: str = (
            dependency_manager
                .convert_filesystem_path(
                    targets=(
                        filesystem_path,
                        ".qlogicae",
                        "solutils",
                        "v1",
                        "plugin",
                    )
                )
        )

        return (
            output
        )

