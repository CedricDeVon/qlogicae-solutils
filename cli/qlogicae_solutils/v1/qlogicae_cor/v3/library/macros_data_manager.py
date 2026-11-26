__all__ = (
    "MacrosDataManager",
)

_ExternalDependencyManager = None
_MacrosDataManager = None

_re = None


def _allocate():
    global _allocate
    global _MacrosDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __MacrosDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "macros"
            })

            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _re  
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _re = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="re"
                    )
                )

            return True

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "selected_identifier_pattern": (
                            _re().compile(r"^[A-Za-z0-9._-]+$")
                        ),
                        "selected_macros_pattern": (
                            _re().compile(r"\$\{\{\s*([A-Za-z0-9._-]+)\s*\}\}")
                        ),
                    }                  
                })
            )

        def read_selected_identifier_pattern(self):
            return (
                self.read_one_data(
                    ("selected_identifier_pattern",)
                )
            )

        def read_selected_macros_pattern(self):
            return (
                self.read_one_data(
                    ("selected_macros_pattern",)
                )
            )


    _MacrosDataManager = __MacrosDataManager
    _allocate = lambda: None


def MacrosDataManager():
    if _MacrosDataManager is None:
        _allocate()

    return _MacrosDataManager
