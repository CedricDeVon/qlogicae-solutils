__all__ = (
    "WorkflowPluginManager",
)

_WorkflowPluginManager = None
_ExternalDependencyManager = None

_WorkflowManager = None
_WorkflowDataManager = None


def _allocate():
    global _allocate
    global _WorkflowPluginManager

    from .base_plugin_manager import BasePluginManager

    class __WorkflowPluginManager(BasePluginManager()):
        def __init__(self):
            super().__init__()

            self.construct()        

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _WorkflowManager
                global _WorkflowDataManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )
                _WorkflowDataManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.workflow_data_manager",
                            member="WorkflowDataManager",
                            is_member_callable=True,
                        )
                )
                _WorkflowManager = (
                    _ExternalDependencyManager()
                        .read_singleton()
                        .import_module(                    
                            path="qlogicae_cor.v3.library.workflow_manager",
                            member="WorkflowManager",
                            is_member_callable=True,
                        )
                )

            self.base_construct({
                "data_manager": _WorkflowDataManager
            })        

            return True

        def run_workflows(self, targets):
            workflow_manager = (
                _WorkflowManager()
                    .read_singleton()
            )

            result = True
            result = (
                workflow_manager.run_workflows({
                    "targets": targets,
                })
            )

            return result


    _WorkflowPluginManager = __WorkflowPluginManager
    _allocate = lambda: None


def WorkflowPluginManager():
    if _WorkflowPluginManager is None:
        _allocate()

    return _WorkflowPluginManager

