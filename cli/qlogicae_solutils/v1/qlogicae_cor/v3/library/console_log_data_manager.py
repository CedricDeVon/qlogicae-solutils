__all__ = (
    "ConsoleLogDataManager",
)

_ConsoleLogDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _ConsoleLogDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __ConsoleLogDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "console_log"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({           
                    "data": {
                        "is_enabled": False,
                        "is_verbose_enabled": True,
                        "log_level": 10,
                        "stack_level": 3,
                    }         
                })
            )


    _ConsoleLogDataManager = __ConsoleLogDataManager
    _allocate = lambda: None


def ConsoleLogDataManager():
    if _ConsoleLogDataManager is None:
        _allocate()

    return _ConsoleLogDataManager
