__all__ = (
    "FunctionStorageManager",
)

_FunctionStorageManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _FunctionStorageManager

    class __FunctionStorageManager:
        __slots__ = (
            "_collection",
        )

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

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            self._collection = {}

            return True

        @property
        def collection(self):
            return self._collection

        @collection.setter
        def collection(self, value):
            if not isinstance(value, dict):
                raise ValueError("")

            self._collection = value

        def setup(self, **kwargs):
            if not kwargs:
                return True
                
            return True

        def shutdown(self):
            return True

        def is_function_found(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("")

            return (
                target in self._collection
            )

        def read_all_functions(self):
            return (
                self._collection
            )

        def read_one_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("")

            command = (
                self._collection.get(
                    target,
                    None
                ) or None
            )
            if not command:
                raise ValueError("")

            return command

        def write_one_function(self, target, callable):
            if not isinstance(target, (str)) or not target:
                raise ValueError("")

            if not callable(callable) or not callable:
                raise ValueError("")

            self._collection[target] = callable        

            return True

        def remove_one_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("")

            del self._collection[target]

            return True

        def run_one_function(self, target, *args, **kwargs):
            if not isinstance(target, (str)) or not target:
                raise ValueError("")

            if not isinstance(args, (tuple, list)):
                raise ValueError("")

            if not isinstance(kwargs, (dict)):
                raise ValueError("")

            command = (
                self._collection.get(
                    target,
                    None
                ) or None
            )
            if not command:
                raise ValueError("")

            result = True
            result = (
                command(
                    *args,
                    **kwargs,
                ) and result
            )

            return result        

        def setup_functions(self, plugin_data):
            if not plugin_data:
                raise ValueError("")

            result = {}
            stack = [
                (command, "")
                for command in reversed(plugin_data)
            ]

            while stack:
                command, prefix = stack.pop()

                if not command:
                    continue

                name = command["name"]

                combination = (
                    f"{prefix}-{name}"
                    if prefix
                    else name
                )

                command_handler = command.get("command_handler")

                if callable(command_handler):
                    result[combination] = command_handler

                subcommands = command.get("subcommands") or ()

                if subcommands:
                    subparser_configuration = (
                        command.get("subparsers") or {}
                    )

                    stack.extend(
                        (subcommand, combination)
                        for subcommand in reversed(subcommands)
                    )

            self._collection = result

            return True


    _FunctionStorageManager = __FunctionStorageManager
    _allocate = lambda: None


def FunctionStorageManager():
    if _FunctionStorageManager is None:
        _allocate()

    return _FunctionStorageManager
