__all__ = (
    "TimestampDataManager",
)

_ExternalDependencyManager = None
_TimestampDataManager = None


def _allocate():
    global _allocate
    global _TimestampDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __TimestampDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "timestamp"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "date_timestamp_format": (
                            "%Y-%m-%dT%H:%M:%S"
                        ),
                        "filesystem_timestamp_format": (
                            "%Y-%m-%dT%H-%M-%S"
                        ),
                    }                  
                })
            )

        def read_date_timestamp_format(self):
            return (
                self.read_one_data(
                    ("date_timestamp_format",),
                ) or "%Y-%m-%dT%H:%M:%S"
            )

        def read_filesystem_timestamp_format(self):
            return (
                self.read_one_data(
                    ("filesystem_timestamp_format",),
                ) or "%Y-%m-%dT%H-%M-%S"
            )


    _TimestampDataManager = __TimestampDataManager
    _allocate = lambda: None


def TimestampDataManager():
    if _TimestampDataManager is None:
        _allocate()

    return _TimestampDataManager
