__all__ = (
    "TextIoPluginManager",
)

_TextIoPluginManager = None
_ExternalDependencyManager = None

_TextIoDataManager = None


def _allocate():
    global _allocate
    global _TextIoPluginManager

    class __TextIoPluginManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _TextIoDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _TextIoDataManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.text_io_data_manager",
                        member="TextIoDataManager",
                        is_member_callable=True,
                    )
            )
            
            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            text_io_data_manager = (
                _TextIoDataManager()
                    .read_singleton()
            )
            
            return (
                text_io_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):
            result = True
            return result

        def run_plugin(self):            
            result = True
            return result


        def shutdown_plugin(self):            
            result = True
            return result


    _TextIoPluginManager = __TextIoPluginManager
    _allocate = lambda: None


def TextIoPluginManager():
    if _TextIoPluginManager is None:
        _allocate()

    return _TextIoPluginManager

