__all__ = (
    "ScriptProcessManager",
)

_ScriptProcessManager = None
_ExternalDependencyManager = None

_shlex = None
_subprocess = None
_TextEncodingDataManager = None


def _allocate():
    global _allocate
    global _ScriptProcessManager

    class __ScriptProcessManager:
        __slots__ = ()

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

            global _shlex
            global _subprocess
            global _TextEncodingDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )
            _shlex = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="shlex",
                )
            )
            _subprocess = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="subprocess",
                )
            )
            _TextEncodingDataManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.text_encoding_data_manager",
                    member="TextEncodingDataManager",
                    is_member_callable=True,
                )
            )
            _ScriptProcessDataManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.script_process_data_manager",
                    member="ScriptProcessDataManager",
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

        def execute_command(
            self,
            command,
        ):
            if not command:
                raise ValueError("")

            script_process_type = (
                _ScriptProcessDataManager()
                    .read_singleton()
                    .read_script_process_type()
            )
            valid_script_process_types = (
                _ScriptProcessDataManager()
                    .read_singleton()
                    .read_valid_script_process_types()
            )

            if script_process_type not in valid_script_process_types:
                return False

            encoding = (
                _TextEncodingDataManager()
                    .read_singleton()
                    .read_selected_encoding_type()
            )

            match script_process_type.lower():
                case "shell":
                    value = _subprocess().run(  # nosec B604
                        command,
                        encoding=encoding,
                        text=True,
                        shell=True,
                    )

                case "subprocess":
                    value = _subprocess().run(
                        _shlex().split(command),
                        encoding=encoding,
                        text=True,
                    )

                case _:
                    raise ValueError("")

            return value


    _ScriptProcessManager = __ScriptProcessManager
    _allocate = lambda: None


def ScriptProcessManager():
    if _ScriptProcessManager is None:
        _allocate()

    return _ScriptProcessManager


# ScriptProcessManager()
