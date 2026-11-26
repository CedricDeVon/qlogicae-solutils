__all__ = (
    "TimestampEnumManager",
)

_TimestampEnumManager = None
_ExternalDependencyManager = None

_Timestamp = None
_EnumConversionValue = None


def _allocate():
    global _allocate
    global _TimestampEnumManager

    from .abstract_manager import AbstractManager

    class __TimestampEnumManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _Timestamp
                global _EnumConversionValue

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _EnumConversionValue = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.enum_conversion_value",
                        member="EnumConversionValue",
                        is_member_callable=True
                    )
                )
                _Timestamp = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.timestamp",
                        member="Timestamp",
                        is_member_callable=True
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
            Timestamp = (
                _Timestamp()
            )

            if output_type is None:
                output_type = EnumConversionValue.STRING

            match output_type:
                case EnumConversionValue.STRING:
                    match input_type:
                        case Timestamp.ISO_DATE_STRING:
                            return "iso_date_string"

                        case Timestamp.ISO_FILESYSTEM_STRING:
                            return "iso_filesystem_string"

                        case _:
                            return "iso_date_string"

                case EnumConversionValue.ENUM:
                    match input_type.lower():
                        case "local":
                            return Timestamp.ISO_DATE_STRING

                        case "iso_filesystem_string":
                            return Timestamp.ISO_FILESYSTEM_STRING

                        case _:
                            return Timestamp.NONE

                case _:
                    return EnumConversionValue.NONE

    _TimestampEnumManager = __TimestampEnumManager
    _allocate = lambda: None


def TimestampEnumManager():
    if _TimestampEnumManager is None:
        _allocate()

    return _TimestampEnumManager


# TimestampEnumManager()
