__all__ = (
    "CliCommandManager",
)

_sys = None
_argparse = None
_CliCommandManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _CliCommandManager


    class __CliCommandManager:
        __slots__ = (
            "_parser",
            "_commands",
            "_command_handler",
            "_parsed_arguments",
            "_command_collection",
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
            global _sys
            global _argparse
            global _ExternalDependencyManager

            from qlogicae_cor.v3.library.external_dependency_manager import (
                ExternalDependencyManager,
            )

            _ExternalDependencyManager = (
                ExternalDependencyManager().get_singleton
            )

            self._parser = None
            self._commands = None
            self._command_handler = None
            self._parsed_arguments = None
            self._command_collection = {}

            return True

        @property
        def command_collection(self):
            return self._command_collection


        @command_collection.setter
        def command_collection(self, value):
            if not isinstance(value, dict):
                raise ValueError(
                    "'command_collection' must be a dictionary"
                )

            self._command_collection = value

        def setup(self, **kwargs):
            if not isinstance(kwargs, (dict)):
                raise ValueError(
                    "'kwargs' must be a dictionary"
                )

            command_data = (
                kwargs.get(
                    "command",
                    {}
                ) or {}
            )
            if not isinstance(command_data, (dict)):
                raise ValueError(
                    "plugin export property 'command' "
                    "must be a dictinoary"
                )

            options = (
                command_data.get(
                    "options",
                    {}
                ) or {}
            )
            if not isinstance(options, (dict)):
                raise ValueError(
                    "plugin export property 'command.options' "
                    "must be a dictionary"
                )

            callbacks = (
                command_data.get(
                    "callbacks",
                    {}
                ) or {}
            )
            if not isinstance(callbacks, (dict)):
                raise ValueError(
                    "plugin export property 'command.callbacks' "
                    "must be a dictionary"
                )

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

            result = True
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

        def setup_parser(self, options):
            if not isinstance(options, dict):
                raise ValueError("'options' must be a dictionary")

            _argparse = (
                _ExternalDependencyManager().import_module(
                    path="argparse",
                )
            )

            parser_args = options.get("args") or ()
            parser_kwargs = options.get("kwargs") or {}

            self._parser = _argparse().ArgumentParser(
                *parser_args,
                **parser_kwargs,
            )

            commands = options.get("commands") or ()

            if not commands:
                return True

            subparser_configuration = options.get("subparsers") or {}

            subparsers = self._parser.add_subparsers(
                *(subparser_configuration.get("args") or ()),
                **(subparser_configuration.get("kwargs") or {}),
            )

            self.setup_subcommands(
                subparsers,
                commands,
            )

            return True

        def setup_subcommands(self, subparsers, commands):
            if not subparsers:
                raise ValueError("'subparsers' must be defined")

            if not commands:
                raise ValueError("'commands' must be defined")

            result = {}
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

                    result[combination] = command_handler

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

            self._command_collection = result

            return True

        def run_parser(self, options):
            if not isinstance(options, (dict)):
                raise ValueError(
                    "'options' must be a dictionary"
                )

            command_data = (
                options.get(
                    "command",
                    {}
                ) or {}
            )
            if not isinstance(command_data, (dict)):
                raise ValueError(
                    "plugin export property 'command' "
                    "must be a dictinoary"
                )

            command_callbacks = (
                command_data.get(
                    "callbacks",
                    {}
                ) or {}
            )
            if not isinstance(command_callbacks, (dict)):
                raise ValueError(
                    "plugin export property 'command.callbacks' "
                    "must be a dictinoary"
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

        def run_command(self, target, *args, **kwargs):
            result = True

            return result

        def read_cli_error_output(self):
            _sys = (
                _ExternalDependencyManager().import_module(
                    path="sys",
                )
            )

            return _sys().stderr

        def read_cli_arguments(self):
            _sys = (
                _ExternalDependencyManager().import_module(
                    path="sys",
                )
            )

            return tuple(_sys().argv[1:])


    _CliCommandManager = __CliCommandManager
    _allocate = lambda: None


def CliCommandManager():
    if _CliCommandManager is None:
        _allocate()

    return _CliCommandManager



# CliCommandManager()
