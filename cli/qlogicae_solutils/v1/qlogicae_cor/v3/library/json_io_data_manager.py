__all__ = (
    "JsonIoDataManager",
)

_ExternalDependencyManager = None
_JsonIoDataManager = None


def _allocate():
    global _allocate
    global _JsonIoDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __JsonIoDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "json"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "properties": {
                            "valid_file_extensions": {".json",},
                            "is_ascii_format_enabled": False,
                            "indent_count": 4,
                            "is_key_sortable": False,
                        },
                    }                  
                })
            )

        def read_valid_file_extensions(self):
            return (
                self.read_one_data(
                    ("properties", "valid_file_extensions",),
                ) or {".json",}
            )

        def read_is_ascii_format_enabled(self):
            return (
                self.read_one_data(
                    ("properties", "is_ascii_format_enabled",),
                ) or False
            )

        def read_indent_count(self):
            return (
                self.read_one_data(
                    ("properties", "indent_count",),
                ) or 4
            )

        def read_is_key_sortable(self):
            return (
                self.read_one_data(
                    ("properties", "is_key_sortable",),
                ) or False
            )


    _JsonIoDataManager = __JsonIoDataManager
    _allocate = lambda: None


def JsonIoDataManager():
    if _JsonIoDataManager is None:
        _allocate()

    return _JsonIoDataManager
