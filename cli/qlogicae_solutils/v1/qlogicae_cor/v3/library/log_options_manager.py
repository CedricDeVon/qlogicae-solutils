__all__ = (
    "LogOptionsManager",
)

_LogOptionsManager = None
_ExternalDependencyManager = None

_logging = None
_LogOptions = None


def _allocate():
    global _allocate
    global _LogOptionsManager

    from .abstract_manager import AbstractManager

    class __LogOptionsManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager
            
            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _logging
                global _LogOptions

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _logging = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="logging",
                    )
                )
                _LogOptions = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.log_options",
                        member="LogOptions",
                        is_member_callable=True,
                    )
                )

            return True

        def generate_modified_defaults(
            self,
            default_log_options,
            log_level=None,
        ):
            if log_level is None:
                log_level = _logging().DEBUG

            value = _LogOptions()(
                is_enabled=default_log_options.is_enabled,
                is_verbose_enabled=(
                    default_log_options.is_verbose_enabled
                ),
                log_level=log_level,
                stack_level=default_log_options.stack_level,
            )

            return value

    _LogOptionsManager = __LogOptionsManager
    _allocate = lambda: None


def LogOptionsManager():
    if _LogOptionsManager is None:
        _allocate()

    return _LogOptionsManager


# LogOptionsManager()
