__all__ = (
    "HardwareDataManager",
)

_HardwareDataManager = None
_ExternalDependencyManager = None

_platform = None


def _allocate():
    global _allocate
    global _HardwareDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __HardwareDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "hardware"
            })

            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager
    
                global _platform

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _platform = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="platform",
                    )
                )

            return True

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "operating_system_type": (
                            _platform().system()
                        ),
                        "instruction_architecture_type": (
                            _platform().machine()
                        ),
                    }                  
                })
            )

        def read_platform(self):
            operating_system_type = (
                self.read_operating_system_type()
            )
            instruction_architecture_type = (
                self.instruction_architecture_type()
            )

            return (
                f"{operating_system_type}_{instruction_architecture_type}"
            )

        def read_operating_system_type(self):
            return (
                self.read_one_data(
                    ("operating_system_type",),
                ) or _platform().system()
            )

        def read_instruction_architecture_type(self):
            return (
                self.read_one_data(
                    ("instruction_architecture_type",),
                ) or _platform().machine()
            )


    _HardwareDataManager = __HardwareDataManager
    _allocate = lambda: None


def HardwareDataManager():
    if _HardwareDataManager is None:
        _allocate()

    return _HardwareDataManager
