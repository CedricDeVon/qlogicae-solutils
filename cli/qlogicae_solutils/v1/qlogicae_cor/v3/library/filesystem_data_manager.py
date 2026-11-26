__all__ = (
    "FilesystemDataManager",
)

_ExternalDependencyManager = None
_FilesystemDataManager = None

_os = None
_pathlib = None


def _allocate():
    global _allocate
    global _FilesystemDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __FilesystemDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "filesystem"
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
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(
                            path="os",
                        )
                )
                _pathlib = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(
                            path="pathlib",
                        )
                )

            return True

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "default_remove_excluded_filesystem_paths": (
                            _pathlib().Path(_os().path.abspath(_os().fspath(
                                _pathlib().Path.cwd()
                            ))),
                        ),
                    }                  
                })
            )

        def read_default_remove_excluded_filesystem_paths(self):
            return (
                self.read_one_data(
                    ("default_remove_excluded_filesystem_paths",),
                )
            )


    _FilesystemDataManager = __FilesystemDataManager
    _allocate = lambda: None


def FilesystemDataManager():
    if _FilesystemDataManager is None:
        _allocate()

    return _FilesystemDataManager
