__all__ = (
    "TextEncodingDataManager",
)

_ExternalDependencyManager = None
_TextEncodingDataManager = None


def _allocate():
    global _allocate
    global _TextEncodingDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __TextEncodingDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "text_encoding"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "selected_encoding_type": "utf-8",
                    }                  
                })
            )

        def read_selected_encoding_type(self):
            return (
                self.read_one_data(
                    ("selected_encoding_type",)
                ) or "utf-8"
            )


    _TextEncodingDataManager = __TextEncodingDataManager
    _allocate = lambda: None


def TextEncodingDataManager():
    if _TextEncodingDataManager is None:
        _allocate()

    return _TextEncodingDataManager
