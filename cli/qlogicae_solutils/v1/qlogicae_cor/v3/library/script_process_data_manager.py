__all__ = (
    "ScriptProcessDataManager",
)

_ExternalDependencyManager = None
_ScriptProcessDataManager = None


def _allocate():
    global _allocate
    global _ScriptProcessDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __ScriptProcessDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "script_process"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "selected_script_process_type": "subprocess",
                        "valid_script_process_types": {
                            "shell",
                            "subprocess",
                        },
                    }                  
                })
            )
        
        def read_selected_script_process_type(self):
            return (
                self.read_one_data(
                    ("selected_script_process_type",),
                ) or "subprocess"
            )

        def read_valid_script_process_types(self):
            return (
                self.read_one_data(
                    ("valid_script_process_types",),
                ) or {
                    "shell",
                    "subprocess",
                }
            )


    _ScriptProcessDataManager = __ScriptProcessDataManager
    _allocate = lambda: None


def ScriptProcessDataManager():
    if _ScriptProcessDataManager is None:
        _allocate()

    return _ScriptProcessDataManager
