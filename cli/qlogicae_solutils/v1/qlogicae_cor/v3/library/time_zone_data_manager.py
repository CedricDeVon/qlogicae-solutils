__all__ = (
    "TimeZoneDataManager",
)

_TimeZoneDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _TimeZoneDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __TimeZoneDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "time_zone"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "selected_time_zone_type": "utc",
                        "valid_time_zone_types": {
                            "utc",
                            "local",
                        },
                    }                  
                })
            )

        def read_selected_time_zone_type(self):
            return (
                self.read_one_data(
                    ("selected_time_zone_type",),
                ) or "utc"
            )

        def read_valid_time_zone_types(self):
            return (
                self.read_one_data(
                    ("valid_time_zone_types",),
                ) or {
                    "utc",
                    "local",
                }
            )


    _TimeZoneDataManager = __TimeZoneDataManager
    _allocate = lambda: None


def TimeZoneDataManager():
    if _TimeZoneDataManager is None:
        _allocate()

    return _TimeZoneDataManager
