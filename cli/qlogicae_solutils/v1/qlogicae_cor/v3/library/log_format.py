__all__ = (
    "LogFormat",
)

_LogFormat = None
_ExternalDependencyManager = None

_logging = None
_TimestampManager = None


def _allocate():
    global _allocate
    global _logging
    global _LogFormat
    global _TimestampManager
    global _ExternalDependencyManager

    import logging

    from .external_dependency_manager import ExternalDependencyManager

    _logging = logging
    _ExternalDependencyManager = (
        ExternalDependencyManager()
    )
    _TimestampManager = (
        _ExternalDependencyManager().get_singleton().import_module(
            path="qlogicae_cor.v3.library.timestamp_manager",
            member="TimestampManager",
            is_member_callable=True,
        )
    )

    class __LogFormat(_logging.Formatter):
        def __init__(self):
            super().__init__()

        def format(self, record):
            timestamp = (
                _TimestampManager()
                    .get_singleton()
                    .generate_current_timestamp()
            )

            return (
                f"[ {timestamp} ] "
                f"[ {record.levelname} ] "
                f"{record.getMessage()}"
            )

    _LogFormat = __LogFormat
    _allocate = lambda: None


def LogFormat():
    if _LogFormat is None:
        _allocate()

    return _LogFormat


# LogFormat()
