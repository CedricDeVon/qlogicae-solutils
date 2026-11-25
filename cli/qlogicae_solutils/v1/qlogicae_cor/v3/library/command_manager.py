__all__ = (
    "CommandManager",
)

_CommandManager = None
_ExternalDependencyManager = None

_argparse = None
_CommandFunctionManager = None


def _allocate():
    global _allocate
    global _CommandManager


    class __CommandManager:
        __slots__ = (
            "_parser",
            "_commands",
            "_command_handler",
            "_parsed_arguments",
        )

        _singleton = None

        def __init__(self):
            self.construct()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.shutdown()

        @classmethod
        def read_singleton(cls):
            if cls._singleton is None:
                cls._singleton = cls()

            return cls._singleton

        def construct(self):
            global _ExternalDependencyManager

            global _argparse
            global _CommandFunctionManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _CommandFunctionManager = (
                _ExternalDependencyManager()
                    .read_singleton()
                    .import_module(
                        path="qlogicae_cor.v3.library.command_function_manager",
                        member="CommandFunctionManager",
                        is_member_callable=True,
                    )
            )

            self._parser = None
            self._commands = None
            self._command_handler = None
            self._parsed_arguments = None

            return True

        def setup(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            options = (
                kwargs.get(
                    "options",
                    {}
                ) or {}
            )
            if not isinstance(options, (dict)):
                raise TypeError("")

            is_parser_enabled = (
                kwargs.get(
                    "is_parser_enabled",
                    True
                )
            )
            if not isinstance(is_parser_enabled, (bool)):
                raise TypeError("")

            callbacks = (
                kwargs.get(
                    "callbacks",
                    {}
                ) or {}
            )
            if not isinstance(callbacks, (dict)):
                raise TypeError("")

            callback_on_pre_setup = (
                callbacks.get(
                    "on_pre_setup",
                    None
                )
            )
            callback_on_post_setup = (
                callbacks.get(
                    "on_post_setup",
                    None
                )
            )

            if (
                callback_on_pre_setup and
                callable(callback_on_pre_setup)
            ):
                callback_on_pre_setup()

            command_function_manager = (
                _CommandFunctionManager()
                    .read_singleton()
            )

            result = True
            result = (
                command_function_manager
                    .setup_functions() and result
            )
            if is_parser_enabled:
                result = (
                    self.setup_parser(
                        options
                    ) and result
                )

            if (
                callback_on_post_setup and
                callable(callback_on_post_setup)
            ):
                callback_on_post_setup()

            return result

        def shutdown(self):
            return True

        def run(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")

            command_callbacks = (
                kwargs.get(
                    "callbacks",
                    {}
                ) or {}
            )

            command_callback_on_pre_run = (
                command_callbacks.get(
                    "on_pre_run",
                    None
                )
            )
            command_callback_on_post_run = (
                command_callbacks.get(
                    "on_post_run",
                    None
                )
            )

            if (
                command_callback_on_pre_run and
                callable(command_callback_on_pre_run)
            ):
                command_callback_on_pre_run()

            result = True
            result = (
                self.setup_parsed_arguments() and result
            )
            result = (
                self.setup_command_handler() and result
            )
            result = (
                self.run_command_handler() and result
            )

            if (
                command_callback_on_post_run and
                callable(command_callback_on_post_run)
            ):
                command_callback_on_post_run()

            return (
                result
            )

        def setup_parser(self, kwargs):
            if not isinstance(kwargs, (dict)):
                raise TypeError("")
                
            _argparse = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="argparse",
                )
            )

            parser_args = kwargs.get("args") or ()
            parser_kwargs = kwargs.get("kwargs") or {}

            self._parser = _argparse().ArgumentParser(
                *parser_args,
                **parser_kwargs,
            )

            commands = kwargs.get("commands") or ()

            if not commands:
                return True

            subparser_configuration = kwargs.get("subparsers") or {}

            subparsers = self._parser.add_subparsers(
                *(subparser_configuration.get("args") or ()),
                **(subparser_configuration.get("kwargs") or {}),
            )

            stack = [
                (subparsers, command, "")
                for command in reversed(commands)
            ]

            while stack:
                parent_subparsers, command, prefix = stack.pop()

                if not command:
                    continue

                name = command["name"]

                combination = (
                    f"{prefix}-{name}"
                    if prefix
                    else name
                )

                command_parser = parent_subparsers.add_parser(
                    name,
                    *(command.get("args") or ()),
                    **(command.get("kwargs") or {}),
                )

                command_handler = command.get("command_handler")

                if callable(command_handler):
                    command_parser.set_defaults(
                        command_handler=command_handler,
                    )

                arguments = command.get("arguments") or ()

                for argument in arguments:
                    command_parser.add_argument(
                        *(argument.get("args") or ()),
                        **(argument.get("kwargs") or {}),
                    )

                subcommands = command.get("subcommands") or ()

                if subcommands:
                    subparser_configuration = (
                        command.get("subparsers") or {}
                    )

                    nested_subparsers = command_parser.add_subparsers(
                        *(subparser_configuration.get("args") or ()),
                        metavar=command.get("metavar") or "",
                        **(subparser_configuration.get("kwargs") or {}),
                    )

                    stack.extend(
                        (nested_subparsers, subcommand, combination)
                        for subcommand in reversed(subcommands)
                    )
                    
            return True

        def setup_parsed_arguments(self):
            arguments = self._parser.parse_args()

            self._parsed_arguments = (
                arguments
            )

            return True

        def setup_command_handler(self):
            self._command_handler = getattr(
                self._parsed_arguments,
                "command_handler",
                None,
            )

            return True

        def run_command_handler(self):
            result = True

            if self._command_handler is not None:
                result = self._command_handler(
                    self._parsed_arguments
                ) and result

            else:
                self._parser.print_help()

            return result


    _CommandManager = __CommandManager
    _allocate = lambda: None


def CommandManager():
    if _CommandManager is None:
        _allocate()

    return _CommandManager


# CommandManager()
