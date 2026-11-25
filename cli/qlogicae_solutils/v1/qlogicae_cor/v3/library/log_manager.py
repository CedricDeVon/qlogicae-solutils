__all__ = (
    "LogManager",
)

_LogManager = None
_ExternalDependencyManager = None

_logging = None
_FileLogManager = None
_ConsoleLogManager = None
_LogOptionsManager = None


def _allocate():
    global _allocate
    global _LogManager

    class __LogManager:
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

            global _logging
            global _FileLogManager
            global _ConsoleLogManager
            global _LogOptionsManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _logging = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="logging",
                )
            )
            _ConsoleLogManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.console_log_manager",
                    member="ConsoleLogManager",
                    is_member_callable=True,
                )
            )
            _FileLogManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.file_log_manager",
                    member="FileLogManager",
                    is_member_callable=True,
                )
            )
            _LogOptionsManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.log_options_manager",
                    member="LogOptionsManager",
                    is_member_callable=True,
                )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            _ConsoleLogManager().read_singleton().shutdown()
            _FileLogManager().read_singleton().shutdown()

            return True

        def log(
            self,
            message,
            console_options,
            file_options,
        ):
            _ConsoleLogManager().read_singleton().log(
                message,
                console_options,
            )

            _FileLogManager().read_singleton().log(
                message,
                file_options,
            )

            return message

        def log_debug(self, message):
            return self.log(
                message,
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _ConsoleLogManager().read_singleton().options,
                    log_level=_logging().DEBUG,
                ),
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _FileLogManager().read_singleton().options,
                    log_level=_logging().DEBUG,
                ),
            )

        def log_info(self, message):
            return self.log(
                message,
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _ConsoleLogManager().read_singleton().options,
                    log_level=_logging().INFO,
                ),
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _FileLogManager().read_singleton().options,
                    log_level=_logging().INFO,
                ),
            )

        def log_warning(self, message):
            return self.log(
                message,
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _ConsoleLogManager().read_singleton().options,
                    log_level=_logging().WARNING,
                ),
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _FileLogManager().read_singleton().options,
                    log_level=_logging().WARNING,
                ),
            )

        def log_error(self, message):
            return self.log(
                message,
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _ConsoleLogManager().read_singleton().options,
                    log_level=_logging().ERROR,
                ),
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _FileLogManager().read_singleton().options,
                    log_level=_logging().ERROR,
                ),
            )

        def log_critical(self, message):
            return self.log(
                message,
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _ConsoleLogManager().read_singleton().options,
                    log_level=_logging().CRITICAL,
                ),
                _LogOptionsManager().read_singleton().generate_modified_defaults(
                    _FileLogManager().read_singleton().options,
                    log_level=_logging().CRITICAL,
                ),
            )

    _LogManager = __LogManager
    _allocate = lambda: None


def LogManager():
    if _LogManager is None:
        _allocate()

    return _LogManager


# LogManager()
