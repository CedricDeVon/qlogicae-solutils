__all__ = (
    "TimeZonePluginManager",
)

_TimeZonePluginManager = None
_ExternalDependencyManager = None

_TimeZoneDataManager = None


def _allocate():
    global _allocate
    global _TimeZonePluginManager

    from .base_plugin_manager import BasePluginManager

    class __TimeZonePluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _TimeZoneDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _TimeZoneDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.time_zone_data_manager",
                            member="TimeZoneDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _TimeZoneDataManager
            })        

            return True


    _TimeZonePluginManager = __TimeZonePluginManager
    _allocate = lambda: None


def TimeZonePluginManager():
    if _TimeZonePluginManager is None:
        _allocate()

    return _TimeZonePluginManager

