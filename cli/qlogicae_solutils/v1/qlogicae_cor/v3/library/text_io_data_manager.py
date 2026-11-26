__all__ = (
    "TextIoDataManager",
)

_ExternalDependencyManager = None
_TextIoDataManager = None


def _allocate():
    global _allocate
    global _TextIoDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __TextIoDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "text_io"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "valid_file_extensions": {".txt",},
                    }                  
                })
            )

        def read_valid_file_extensions(self):
            return (
                self.read_one_data(
                    ("valid_file_extensions",),
                ) or {".txt",}
            )


    _TextIoDataManager = __TextIoDataManager
    _allocate = lambda: None


def TextIoDataManager():
    if _TextIoDataManager is None:
        _allocate()

    return _TextIoDataManager
