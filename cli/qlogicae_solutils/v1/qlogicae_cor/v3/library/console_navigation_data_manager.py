__all__ = (
    "ConsoleNavigationDataManager",
)

_ExternalDependencyManager = None
_ConsoleNavigationDataManager = None

_os = None
_pathlib = None


def _allocate():
    global _allocate
    global _ConsoleNavigationDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __ConsoleNavigationDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "console_navigation"
            })

            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager
                
                global _os
                global _pathlib

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _os = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="os"
                    )
                )
                _pathlib = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="pathlib"
                    )
                )

            return True

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({           
                    "data": {
                        "original_executing_filesystem_path": (
                            _pathlib().Path.cwd().resolve()
                        ),
                        "previous_executing_filesystem_path": (
                            ""
                        ),
                        "current_executing_filesystem_path": (
                            _pathlib().Path.cwd().resolve()
                        ),
                        "original_executing_script_filesystem_path": (
                            _pathlib().Path(__file__).resolve()
                        ),
                    }         
                })
            )

        def read_original_executing_filesystem_path(self):
            return (
                self.read_one_data(
                    ("original_executing_filesystem_path",),
                ) or _pathlib().Path.cwd().resolve()
            )

        def read_previous_executing_filesystem_path(self):
            return (
                self.read_one_data(
                    ("previous_executing_filesystem_path",),
                ) or ""
            )

        def read_current_executing_filesystem_path(self):
            return (
                self.read_one_data(
                    ("current_executing_filesystem_path",),
                ) or _pathlib().Path.cwd().resolve()
            )

        def read_original_executing_script_filesystem_path(self):
            return (
                self.read_one_data(
                    ("original_executing_script_filesystem_path",),
                ) or _pathlib().Path(__file__).resolve()
            )

        def write_original_executing_filesystem_path(self, value):
            if not isinstance(value, (str, _pathlib().Path,)):
                raise TypeError("")

            return (
                self.write_one_data(
                    ("original_executing_filesystem_path",),
                    value,
                )
            )

        def write_previous_executing_filesystem_path(self, value):
            if not isinstance(value, (str, _pathlib().Path,)):
                raise TypeError("")

            return (
                self.write_one_data(
                    ("previous_executing_filesystem_path",),
                    value,
                )
            )

        def write_current_executing_filesystem_path(self, value):
            if not isinstance(value, (str, _pathlib().Path,)):
                raise TypeError("")

            return (
                self.write_one_data(
                    ("current_executing_filesystem_path",),
                    value,
                )
            )

        def write_original_executing_script_filesystem_path(self, value):
            if not isinstance(value, (str, _pathlib().Path,)):
                raise TypeError("")

            return (
                self.write_one_data(
                    ("original_executing_script_filesystem_path",),
                    value,
                )
            )


    _ConsoleNavigationDataManager = __ConsoleNavigationDataManager
    _allocate = lambda: None


def ConsoleNavigationDataManager():
    if _ConsoleNavigationDataManager is None:
        _allocate()

    return _ConsoleNavigationDataManager
