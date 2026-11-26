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

    from .base_plugin_manager import BasePluginManager

    class __CommandPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager
            global _CommandDataManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _CommandManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _CommandManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.command_manager",
                            member="CommandManager",
                            is_member_callable=True,
                        )
                )
                _CommandDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.command_data_manager",
                            member="CommandDataManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _CommandDataManager
            })

            return True

        def setup_plugin_hook(self):
            command_data_manager = (
                _CommandDataManager()
                    .read_singleton()
            )
            command_manager = (
                _CommandManager()
                    .read_singleton()
            )

            result = True
            result = (
                command_manager
                    .setup(
                        command_data_manager.read_all_data()
                        
                    ) and result
            )

            return result

        def run_plugin_hook(self):       
            command_data_manager = (
                _CommandDataManager()
                    .read_singleton()
            )
            command_manager = (
                _CommandManager()
                    .read_singleton()
            )

            result = True
            result = (
                command_manager
                    .run(
                        command_data_manager.read_all_data()                        
                    ) and result
            )

            return result


    _CommandPluginManager = __CommandPluginManager
    _allocate = lambda: None


def CommandPluginManager():
    if _CommandPluginManager is None:
        _allocate()

    return _CommandPluginManager

