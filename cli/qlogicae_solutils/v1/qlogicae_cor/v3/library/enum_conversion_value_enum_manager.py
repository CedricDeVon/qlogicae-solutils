__all__ = (
    "EnumConversionValueEnumManager",
)

_EnumConversionValue = None
_EnumConversionValueEnumManager = None
_ExternalDependencyManager = None


def _allocate():
    global _allocate
    global _EnumConversionValueEnumManager

    from .abstract_manager import AbstractManager

    class __EnumConversionValueEnumManager(AbstractManager()):        
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager
                
                global _EnumConversionValue

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _EnumConversionValue = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.enum_conversion_value",
                        member="EnumConversionValue",
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

            if output_type is None:
                output_type = EnumConversionValue.STRING

            match output_type:
                case EnumConversionValue.STRING:
                    match input_type:
                        case EnumConversionValue.STRING:
                            return "string"

                        case EnumConversionValue.ENUM:
                            return "enum"

                        case EnumConversionValue.CUSTOM:
                            return "custom"

                        case _:
                            return "none"

                case EnumConversionValue.ENUM:
                    match str(input_type).lower():
                        case "string":
                            return EnumConversionValue.STRING

                        case "none":
                            return EnumConversionValue.ENUM

                        case "custom":
                            return EnumConversionValue.CUSTOM

                        case _:
                            return EnumConversionValue.NONE

                case _:
                    return EnumConversionValue.NONE


    _EnumConversionValueEnumManager = __EnumConversionValueEnumManager
    _allocate = lambda: None


def EnumConversionValueEnumManager():
    if _EnumConversionValueEnumManager is None:
        _allocate()

    return _EnumConversionValueEnumManager


# EnumConversionValueEnumManager()
