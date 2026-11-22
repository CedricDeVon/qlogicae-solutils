__all__ = (
    "WorkflowPluginManager",
)

_WorkflowPluginManager = None

_PluginManager = None
_WorkflowPropertyManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _WorkflowPluginManager

    class __WorkflowPluginManager:
        __slots__ = (
            "_key_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def key_path(self):
            return self._key_path

        @key_path.setter
        def key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._key_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _PluginManager
            global _WorkflowPropertyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _WorkflowPropertyManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.workflow_property_manager",
                        member="WorkflowPropertyManager",
                        is_member_callable=True,
                    )
            )
            _PluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_manager",
                        member="PluginManager",
                        is_member_callable=True,
                    )
            )

            self._key_path = (
                "qlogicae",
                "cor",
                "v3",
                "workflow",
            )
            
            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def export_plugin(self):
            moduli_plugin_manager = (
                _PluginManager()
                    .get_singleton()
            )
            workflow_property_manager = (
                _WorkflowPropertyManager()
                    .get_singleton()
            )
            
            initial_data = (
                moduli_plugin_manager
                    .setup_data(
                        moduli={ "layer": 0 },
                        key_path=self._key_path,
                        data=(
                            workflow_property_manager
                                .read_initial_data()
                        )
                    )
            )

            return initial_data

        def setup_plugin(self):
            result = True
            return result

        def run_plugin(self):            
            result = True
            return result

        def shutdown_plugin(self):            
            result = True
            return result

        def read_data(self):
            moduli_plugin_manager = (
                _PluginManager()
                    .get_singleton()
            )

            return (
                moduli_plugin_manager
                    .read_data(
                        keys=self._key_path,
                    )
            )


    _WorkflowPluginManager = __WorkflowPluginManager
    _allocate = lambda: None


def WorkflowPluginManager():
    if _WorkflowPluginManager is None:
        _allocate()

    return _WorkflowPluginManager



# PluginManager()

