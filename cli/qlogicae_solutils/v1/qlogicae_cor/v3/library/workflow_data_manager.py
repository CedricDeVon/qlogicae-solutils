__all__ = (
    "WorkflowDataManager",
)

_WorkflowDataManager = None
_ExternalDependencyManager = None

_PluginDataManager = None


def _allocate():
    global _allocate
    global _WorkflowDataManager

    class __WorkflowDataManager:
        __slots__ = (
            "_root_key_path",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @property
        def root_key_path(self):
            return self._root_key_path

        @root_key_path.setter
        def root_key_path(self, value):
            if not isinstance(value, (tuple, list)):
                raise ValueError("")

            self._root_key_path = value

        @classmethod
        def get_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            self._root_key_path = (
                "qlogicae_cor_v3_workflow"
            )            

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            return True

        def shutdown(self):
            return True

        def setup_plugin_data(self):
            global _PluginDataManager

            _PluginDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.plugin_data_manager",
                        member="PluginDataManager",
                        is_member_callable=True,
                    )
            )

            plugin_data_manager = (
                _PluginDataManager().get_singleton()
            )

            return (
                plugin_data_manager
                    .setup_plugin_data({
                        "root_key_path": self._root_key_path,
                        "layer": 0,
                        "data": (
                            {
                                "selection": {},
                                "callbacks": {
                                    "on_pre_run": None,
                                    "on_post_run": None,
                                },
                            }
                        )
                    })
            )

        def read_all_data(
            self
        ):
            data = (
                _PluginDataManager()
                    .get_singleton()
                    .read_all_data(
                        self._root_key_path
                    )
            )

            return (
                data
            )

        def read_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            data = (
                _PluginDataManager()
                    .get_singleton()
                    .read_one_data(
                        self._root_key_path,
                        key_path
                    )
            )

            return (
                data
            )

        def write_all_data(
            self,
            value
        ):
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .write_all_data(
                        self._root_key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def write_one_data(
            self,
            key_path,
            value,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .write_one_data(
                        self._root_key_path,
                        key_path,
                        value
                    ) and result
            )

            return (
                result
            )

        def remove_one_data(
            self,
            key_path,
        ):
            if not isinstance(key_path, (tuple, list)):
                raise TypeError("")
            
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .remove_one_data(
                        self._root_key_path,
                        key_path,
                    ) and result
            )

            return (
                result
            )

        def remove_all_data(
            self,
        ):
            result = True
            result = (
                _PluginDataManager()
                    .get_singleton()
                    .remove_all_data(
                        self._root_key_path,
                    ) and result
            )

            return (
                result
            )

        def read_property(self, data, property_name):
            if not isinstance(data, (dict)):
                raise ValueError("")

            if not isinstance(property_name, (str)):
                raise ValueError("")

            match property_name:
                case "workflow":
                    return (
                        data.get("workflowp_mana", {}) or {}
                    )

                case "is_enabled":
                    return (
                        data.get("is_enabled", True)
                    )

                case "is_failure_optional":
                    return (
                        data.get("is_failure_optional", False)
                    )

                case "platforms_included":
                    return (
                        data.get("platforms_included", set()) or set()
                    )

                case "platforms_excluded":
                    return (
                        data.get("platforms_excluded", set()) or set()
                    )

                case "successful_return_codes":
                    return (
                        data.get("successful_return_codes", set()) or set()
                    )

                case "unsuccessful_return_codes":
                    return (
                        data.get("unsuccessful_return_codes", set()) or set()
                    )

                case "process":
                    return (
                        data.get("process", "subprocess") or "subprocess"
                    )

                case "delay":
                    return (
                        data.get("delay", 0) or 0
                    )

                case "selection":
                    return (
                        data.get("selection", {}) or {}
                    )

                case "jobs":
                    return (
                        data.get("jobs", tuple()) or tuple()
                    )

                case "run":
                    return (
                        data.get("run", "") or ""
                    )

                case "arguments":
                    return (
                        data.get("arguments", {}) or {}
                    )

                case "args":
                    return (
                        data.get("args", tuple()) or tuple()
                    )

                case "kwargs":
                    return (
                        data.get("kwargs", {}) or {}
                    )

                case _:
                    raise ValueError("")


    _WorkflowDataManager = __WorkflowDataManager
    _allocate = lambda: None


def WorkflowDataManager():
    if _WorkflowDataManager is None:
        _allocate()

    return _WorkflowDataManager
