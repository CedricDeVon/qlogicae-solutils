__all__ = (
    "FileLogDataManager",
)

_FileLogDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FileLogDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __FileLogDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "file_log"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "log_level": 10,
                        "stack_level": 3,
                        "is_enabled": False,
                        "is_verbose_enabled": True,
                        "target_filesystem_paths": [],
                    }                  
                })
            )


    _FileLogDataManager = __FileLogDataManager
    _allocate = lambda: None


def FileLogDataManager():
    if _FileLogDataManager is None:
        _allocate()

    return _FileLogDataManager
