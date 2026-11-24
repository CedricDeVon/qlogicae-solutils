__all__ = (
    "CommandFunctionManager",
)

_CommandFunctionManager = None
_ExternalDependencyManager = None

_CommandDataManager = None


def _allocate():
    global _allocate
    global _CommandFunctionManager

    class __CommandFunctionManager:
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
            global _CommandDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _CommandDataManager = (
                _ExternalDependencyManager()
                    .get_singleton()
                    .import_module(
                        path="qlogicae_cor.v3.library.command_data_manager",
                        member="CommandDataManager",
                        is_member_callable=True,
                    )
            )

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                return True
                
            return True

        def shutdown(self):
            return True

        def is_function_found(self, target):
            if not isinstance(target, (str)) or not target:
                raise TypeError("")

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            collection = (
                command_data_manager
                    .read_one_data(
                        ("functions",)
                    )
            )

            return (
                target in collection
            )

        def read_all_functions(self):
            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            return (
                command_data_manager
                    .read_one_data(
                        ("functions",)
                    )
            )

        def read_one_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise TypeError("")

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            command = (
                command_data_manager
                    .read_one_data(
                        ("functions", target,)
                    )
            )
            if not callable(command):
                raise TypeError("")

            return command

        def write_one_function(self, target, callable):
            if not isinstance(target, (str)) or not target:
                raise TypeError("")

            if not callable(callable) or not callable:
                raise TypeError("")

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            command_data_manager.write_one_data(
                ("functions", target),
                target
            )

            return True

        def remove_one_function(self, target):
            if not isinstance(target, (str)) or not target:
                raise TypeError("")

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            command_data_manager.remove_one_data(
                ("functions", target),
            )

            return True

        def run_one_function(self, target, *args, **kwargs):
            if not isinstance(target, (str)) or not target:
                raise TypeError("")

            if not isinstance(args, (tuple, list)):
                raise TypeError("")

            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )

            command = (
                command_data_manager
                    .read_one_data(
                        ("functions", target,)
                    )
            )
            if not callable(command):
                raise TypeError("")

            result = True
            result = (
                command(
                    *args,
                    **kwargs,
                ) and result
            )

            return result        

        def setup_functions(self):
            command_data_manager = (
                _CommandDataManager()
                    .get_singleton()                    
            )
            commands = (
                command_data_manager.read_one_data(
                    ("options", "commands",)
                )
            )

            result = {}
            stack = [
                (command, "")
                for command in reversed(commands)
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

            command_data_manager.write_one_data(
                ("functions", ),
                result
            )

            return True


    _CommandFunctionManager = __CommandFunctionManager
    _allocate = lambda: None


def CommandFunctionManager():
    if _CommandFunctionManager is None:
        _allocate()

    return _CommandFunctionManager
