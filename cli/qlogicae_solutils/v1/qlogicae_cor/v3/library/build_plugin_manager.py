__all__ = (
    "BuildManager",
)

_BuildPluginManager = None
_ExternalDependencyManager = None

_PluginManager = None
_BuildManager = None


def _allocate():
    global _allocate
    global _BuildPluginManager

    class __BuildPluginManager:
        __slots__ = (
            "_data_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def data_path(self):
            return self._data_path

        @data_path.setter
        def data_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise TypeError(
                    "'tuple' or 'list' types required"
                )

            self._data_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _PluginManager
            global _BuildManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
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
            _BuildManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.build_manager",
                        member="BuildManager",
                        is_member_callable=True,
                    )
            )

            self._data_path = (
                "qlogicae",
                "cor",
                "v3",
                "build",
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
            build_manager = (
                _BuildManager()
                    .get_singleton()
            )
            
            initial_data = (
                moduli_plugin_manager
                    .setup_data(
                        moduli={ "layer": 0 },
                        key_path=self._key_path,
                        data=(
                            build_manager.read_all_items()
                        ),
                    )
            )

            return initial_data

        def setup_plugin(self):
            build_manager = (
                _BuildManager()
                    .get_singleton()
            )

            plugin_data = (
                self.read_data()
            )

            plugin_data_build = (
                plugin_data.get(
                    "build",
                    {}
                ) or {}
            )        

            result = True     
            result = (
                build_manager.write_all_items(
                    plugin_data_build
                )
            )

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
                        keys=self._data_path,
                    )
            )

    _BuildPluginManager = __BuildPluginManager
    _allocate = lambda: None


def BuildPluginManager():
    if _BuildPluginManager is None:
        _allocate()

    return _BuildPluginManager
