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

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

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
                raise ValueError(
                    "'collection' must be a dictionary"
                )

            self._collection = value

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError(
                    "'kwargs' must be a dictionary"
                )

            return True

        def shutdown(self):
            return True

        def is_function_found(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("'target' must be a non-empty string")

            return (
                target in self._collection
            )

        def read_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("'target' must be a non-empty string")

            command = (
                self._collection.get(
                    target,
                    None
                ) or None
            )
            if not command:
                raise ValueError(f"'{target}' function does not exist")

            return command

        def write_function(self, target, callable):
            if not isinstance(target, (str)) or not target:
                raise ValueError("'target' must be a non-empty string")

            if not callable(callable) or not callable:
                raise ValueError("'callable' must be a non-empty function")

            self._collection[target] = callable        

            return True

        def remove_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise ValueError("'target' must be a non-empty string")

            del self._collection[target]

            return True

        def run_function(self, target, *args, **kwargs):
            if not isinstance(target, (str)) or not target:
                raise ValueError("'target' must be a non-empty string")

            if not isinstance(args, (tuple, list)):
                raise ValueError("'args' must either be a tuple or list")

            if not isinstance(kwargs, (dict)):
                raise ValueError("'kwargs' must be a dictionary")

            command = (
                self._collection.get(
                    target,
                    None
                ) or None
            )
            if not command:
                raise ValueError(f"'{target}' function does not exist")

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
                raise ValueError("'plugin_data' must be defined")

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
