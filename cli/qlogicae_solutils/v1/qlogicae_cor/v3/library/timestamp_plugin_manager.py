__all__ = (
    "TimestampPluginManager",
)

_ExternalDependencyManager = None
_TimestampPluginManager = None

_TimestampDataManager = None


def _allocate():
    global _allocate
    global _TimestampPluginManager

    from .base_plugin_manager import BasePluginManager

    class __TimestampPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _TimestampDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _TimestampDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.timestamp_data_manager",
                            member="TimestampDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _TimestampDataManager
            })        

            return True


    _TimestampPluginManager = __TimestampPluginManager
    _allocate = lambda: None


def TimestampPluginManager():
    if _TimestampPluginManager is None:
        _allocate()

    return _TimestampPluginManager
