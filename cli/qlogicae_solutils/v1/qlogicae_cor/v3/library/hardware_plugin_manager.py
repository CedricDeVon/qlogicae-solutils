__all__ = (
    "HardwarePluginManager",
)

_HardwarePluginManager = None

_HardwareDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _HardwarePluginManager

    from .base_plugin_manager import BasePluginManager

    class __HardwarePluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _HardwareDataManager
                
                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _HardwareDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.hardware_data_manager",
                            member="HardwareDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _HardwareDataManager
            })        

            return True


    _HardwarePluginManager = __HardwarePluginManager
    _allocate = lambda: None


def HardwarePluginManager():
    if _HardwarePluginManager is None:
        _allocate()

    return _HardwarePluginManager


