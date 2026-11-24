__all__ = (
    "CommandPluginManager",
)

_CommandPluginManager = None
_ExternalDependencyManager = None

_CommandManager = None
_CommandDataManager = None


def _allocate():
    global _allocate
    global _CommandPluginManager

    class __CommandPluginManager:
        __slots__ = ()

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _CommandManager
            global _CommandDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _CommandManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.command_manager",
                        member="CommandManager",
                        is_member_callable=True,
                    )
            )
            _CommandDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.command_data_manager",
                        member="CommandDataManager",
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
            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()
            )
            
            return (
                command_data_manager
                    .setup_plugin_data()
            )

        def setup_plugin(self):
            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()
            )
            command_manager = (
                _CommandManager()
                    .get_singleton()
            )

            result = True
            result = (
                command_manager
                    .setup(
                        command_data_manager.read_all_data()
                        
                    ) and result
            )

            return result

        def run_plugin(self):       
            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()
            )
            command_manager = (
                _CommandManager()
                    .get_singleton()
            )

            result = True
            result = (
                command_manager
                    .run(
                        command_data_manager.read_all_data()
                        
                    ) and result
            )

            return result

        def shutdown_plugin(self):            
            result = True
            return result


    _CommandPluginManager = __CommandPluginManager
    _allocate = lambda: None


def CommandPluginManager():
    if _CommandPluginManager is None:
        _allocate()

    return _CommandPluginManager

