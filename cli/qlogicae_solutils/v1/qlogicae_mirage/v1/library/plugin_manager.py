__all__ = (
    "PluginManager",
)

_PluginManager = None
_ModuliPluginManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _PluginManager

    class __PluginManager:
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
                raise ValueError(
                    "'value' must be a tuple or list"
                )

            self._data_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ModuliPluginManager
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _ModuliPluginManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_moduli.v1.library.plugin_manager",
                        member="PluginManager",
                        is_member_callable=True,
                    )
            )

            self._data_path = (
                "qlogicae",
                "mirage",
                "v1",
            )
            
            return True

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            return True

        def shutdown(self):
            return True

        def export(self):
            moduli_plugin_manager = (
                _ModuliPluginManager()
                    .get_singleton()
            )
            
            initial_data = (
                moduli_plugin_manager
                    .setup_data(
                        keys=self._data_path,
                        merge_layer=0,
                        data={
                            "workflow": {
                                "selection": {},
                                "callbacks": {
                                    "on_pre_run": None,
                                    "on_post_run": None,
                                },
                            },
                            "callbacks": {
                                "on_pre_run": None,
                                "on_post_run": None,
                                "on_pre_setup": None,
                                "on_post_setup": None,
                            },
                        },
                    )
            )

            return initial_data

        def read_data(self):
            moduli_plugin_manager = (
                _ModuliPluginManager()
                    .get_singleton()
            )

            return (
                moduli_plugin_manager
                    .read_data(
                        keys=self._data_path,
                    )
            )


    _PluginManager = __PluginManager
    _allocate = lambda: None


def PluginManager():
    if _PluginManager is None:
        _allocate()

    return _PluginManager



# PluginManager()

# _data = {
#     "qlogicae": {
#         "solutils": {
#             "v1": {
#                 "workflow": {
#                     "selection": {
#                         "qlogicae-project-stage-release": {
#                             "filesystem-path": "",
#                             "scripts": [
#                                 {
#                                     "run": "echo 'qlogicae-project-stage-release'",
#                                 },
#                                 {
#                                     "run": "qlogicae-project-build",
#                                 },
#                                 {
#                                     "run": print_message,
#                                     "args": [
#                                         "Hello"
#                                     ],
#                                     "kwargs": {
#                                         "key": "value"
#                                     },
#                                 },
#                                 {
#                                     "run": "filesystem-create",
#                                     "kwargs": {
#                                         "target_filesystem_paths": [
#                                             "output",
#                                         ],
#                                     },
#                                     "is-enabled": True,
#                                     "is-failure-optional": True,
#                                     "platforms-included": set(), # "Linux-x86_64"
#                                     "platforms-excluded": set(),
#                                     "return-codes-successful": set(), # 0
#                                     "return-codes-unsuccessful": set(), # 1, -1
#                                     "delay": 1,
#                                     "delay-time-unit": "ms",
#                                     "is-asynchronous": True,
#                                 },
#                             ],
#                             "is-enabled": True,
#                             "is-failure-optional": True,
#                             "platforms-included": set(), # "Linux-x86_64"
#                             "platforms-excluded": set(),
#                             "return-codes-successful": set(), # 0
#                             "return-codes-unsuccessful": set(), # 1, -1
#                             "delay": 1,
#                             "delay-time-unit": "ms",
#                             "is-asynchronous": True,
#                         },
#                         "qlogicae-project-build": {
#                             "filesystem-path": "",
#                             "scripts": [
#                                 {
#                                     "run": {
#                                         "value": "echo 'qlogicae-project-build'",
#                                     },
#                                 },
#                             ],
#                         },
#                     },
#                 },
#             }
#         }
#     }
# }

