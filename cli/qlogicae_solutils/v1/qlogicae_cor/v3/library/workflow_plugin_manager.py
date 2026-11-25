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

    class __WorkflowPluginManager:
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

            global _WorkflowManager
            global _WorkflowDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _WorkflowDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.workflow_data_manager",
                        member="WorkflowDataManager",
                        is_member_callable=True,
                    )
            )
            _WorkflowManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.workflow_manager",
                        member="WorkflowManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def run_workflows(self, targets):
            workflow_manager = (
                _WorkflowManager()
                    .get_singleton()
            )

            result = True
            result = (
                workflow_manager.run_workflows({
                    "targets": targets,
                })
            )

            return result

        def export_plugin(self):
            workflow_data_manager = (
                _WorkflowDataManager()
                    .get_singleton()
            )
            
            return (
                workflow_data_manager
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


    _WorkflowPluginManager = __WorkflowPluginManager
    _allocate = lambda: None


def WorkflowPluginManager():
    if _WorkflowPluginManager is None:
        _allocate()

    return _WorkflowPluginManager

