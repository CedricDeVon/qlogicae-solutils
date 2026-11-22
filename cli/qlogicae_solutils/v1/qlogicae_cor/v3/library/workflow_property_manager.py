__all__ = (
    "WorkflowPropertyManager",
)

_SystemManager = None
_WorkflowPropertyManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _WorkflowPropertyManager

    class __WorkflowPropertyManager:
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
            global _SystemManager
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _SystemManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(                    
                        path="qlogicae_cor.v3.library.system_manager",
                        member="SystemManager",
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

        def read_initial_data(self):
            data = {
                "selection": {},
                "callbacks": {
                    "on_pre_run": None,
                    "on_post_run": None,
                },
            }

            return (
                data
            )

        def read_property(self, data, property_name):
            if not isinstance(data, (dict)):
                raise ValueError("")

            if not isinstance(property_name, (str)):
                raise ValueError("")

            match property_name:
                case "workflow":
                    return (
                        data.get("workflow", {}) or {}
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


    _WorkflowPropertyManager = __WorkflowPropertyManager
    _allocate = lambda: None


def WorkflowPropertyManager():
    if _WorkflowPropertyManager is None:
        _allocate()

    return _WorkflowPropertyManager
