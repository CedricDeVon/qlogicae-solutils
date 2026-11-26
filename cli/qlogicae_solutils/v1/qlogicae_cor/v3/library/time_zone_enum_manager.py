__all__ = (
    "TimeZoneEnumManager",
)

_TimeZoneEnumManager = None
_ExternalDependencyManager = None

_datetime = None
_TimeZone = None
_EnumConversionValue = None


def _allocate():
    global _allocate
    global _TimeZoneEnumManager

    from .abstract_manager import AbstractManager

    class __TimeZoneEnumManager(AbstractManager()):
        def __init__(self):
            self.construct()

        def construct(self):
            global _ExternalDependencyManager
            
            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _datetime
                global _TimeZone
                global _EnumConversionValue

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _datetime = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="datetime",
                    )
                )
                _EnumConversionValue = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.enum_conversion_value",
                        member="EnumConversionValue",
                        is_member_callable=True,
                    )
                )
                _TimeZone = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.time_zone",
                        member="TimeZone",
                        is_member_callable=True,
                    )
                )

            return True

        def convert_value(
            self,
            input_type,
            output_type=None,
        ):
            TimeZone = (
                _TimeZone()
            )
            EnumConversionValue = (
                _EnumConversionValue()
            )

            if output_type is None:
                output_type = EnumConversionValue.STRING

            match output_type:
                case EnumConversionValue.STRING:
                    match input_type:
                        case TimeZone.LOCAL:
                            return "local"

                        case TimeZone.UTC:
                            return "utc"

                        case TimeZone.CUSTOM:
                            return "custom"

                        case _:
                            return "local"

                case EnumConversionValue.ENUM:
                    match str(input_type).lower():
                        case "local":
                            return TimeZone.LOCAL

                        case "utc":
                            return TimeZone.UTC

                        case "custom":
                            return TimeZone.CUSTOM

                        case _:
                            return TimeZone.LOCAL

                case EnumConversionValue.CUSTOM:
                    match str(input_type).lower():
                        case "local":
                            return _datetime().datetime.now().astimezone().tzinfo

                        case "utc":
                            return _datetime().UTC

                        case "custom":
                            return _datetime().datetime.now().astimezone().tzinfo

                        case _:
                            return _datetime().datetime.now().astimezone().tzinfo

                case _:
                    return EnumConversionValue.NONE

    _TimeZoneEnumManager = __TimeZoneEnumManager
    _allocate = lambda: None


def TimeZoneEnumManager():
    if _TimeZoneEnumManager is None:
        _allocate()

    return _TimeZoneEnumManager

# TimeZoneEnumManager()
