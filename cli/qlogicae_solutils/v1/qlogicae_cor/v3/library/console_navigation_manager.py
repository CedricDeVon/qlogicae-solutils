__all__ = (
    "ConsoleNavigationManager",
)

_ConsoleNavigationManager = None
_ExternalDependencyManager = None

_os = None
_pathlib = None
_ConsoleNavigationDataManager = None


def _allocate():
    global _allocate
    global _ConsoleNavigationManager

    class __ConsoleNavigationManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _os
            global _pathlib
            global _ConsoleNavigationDataManager

            from .external_dependency_manager import ExternalDependencyManager

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
            _ConsoleNavigationDataManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.console_navigation_data_manager",
                    member="ConsoleNavigationDataManager",
                    is_member_callable=True
                )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True
                
            return True

        def shutdown(self):
            return True

        def navigate(self, filesystem_path):
            if not isinstance(filesystem_path, (str, _pathlib().Path)):
                raise TypeError("")

            console_navigation_data_manager = (
                _ConsoleNavigationDataManager()
                    .read_singleton()
            )

            console_navigation_data_manager.write_previous_executing_filesystem_path(
                console_navigation_data_manager
                    .read_current_executing_filesystem_path()
            )

            filesystem_path = (
                _pathlib()
                    .Path(filesystem_path)
                    .expanduser()
                    .resolve()
            )

            console_navigation_data_manager.write_current_executing_filesystem_path(
                filesystem_path
            )

            _os().chdir(
                filesystem_path
            )

            return True


    _ConsoleNavigationManager = __ConsoleNavigationManager
    _allocate = lambda: None


def ConsoleNavigationManager():
    if _ConsoleNavigationManager is None:
        _allocate()

    return _ConsoleNavigationManager

# ConsoleNavigationManager().read_singleton()
