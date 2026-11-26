__all__ = (
    "ScriptProcessEnumManager",
)

_ScriptProcessEnumManager = None
_ExternalDependencyManager = None

_ScriptProcess = None
_EnumConversionValue = None


def _allocate():
    global _allocate
    global _ScriptProcessEnumManager

    from .abstract_manager import AbstractManager

    class __ScriptProcessEnumManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _ScriptProcess
                global _EnumConversionValue

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _EnumConversionValue = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.enum_conversion_value",
                        member="EnumConversionValueScriptProcess",
                        is_member_callable=True,
                    )
                )
                _ScriptProcess = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.script_process",
                        member="ScriptProcess",
                        is_member_callable=True,
                    )
                )

            return True

        def convert_value(
            self,
            input_type,
            output_type=None,
        ):
            EnumConversionValue = (
                _EnumConversionValue()
            )
            ScriptProcess = (
                _ScriptProcess()
            )

            if output_type is None:
                output_type = EnumConversionValue.STRING

            match output_type:
                case EnumConversionValue.STRING:
                    match input_type:
                        case ScriptProcess.SHELL:
                            return "shell"

                        case ScriptProcess.SUBPROCESS:
                            return "subprocess"

                        case _:
                            return "none"

                case EnumConversionValue.ENUM:
                    match str(input_type).lower():
                        case "shell":
                            return ScriptProcess.SHELL

                        case "subprocess":
                            return ScriptProcess.SUBPROCESS

                        case _:
                            return ScriptProcess.SUBPROCESS

                case _:
                    return EnumConversionValue.NONE


    _ScriptProcessEnumManager = __ScriptProcessEnumManager
    _allocate = lambda: None


def ScriptProcessEnumManager():
    if _ScriptProcessEnumManager is None:
        _allocate()

    return _ScriptProcessEnumManager


# ScriptProcessEnumManager()
