__all__ = (
    "WorkflowDataManager",
)

_WorkflowDataManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _WorkflowDataManager

    from .base_data_manager import (
        BaseDataManager
    )

    class __WorkflowDataManager(BaseDataManager()):
        def __init__(self):
            super().__init__({
                "sub_root_key_path": "workflow"
            })

        def setup_plugin_data(self):
            return (
                self.base_setup_plugin_data({ 
                    "data": {
                        "selection": {},
                    }                  
                })
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
