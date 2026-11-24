__all__ = (
    "TimeZoneManager",
)

_TimeZoneManager = None
_ExternalDependencyManager = None

_TimeDataManager = None
_EnumConversionValue = None
_TimeZoneEnumManager = None

def _allocate():
    global _allocate
    global _TimeZoneManager

    class __TimeZoneManager:
        __slots__ = (
            "_selected_time_zone_type",
            "_valid_time_zone_types",
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

        @property
        def selected_time_zone_type(self):
            return self._selected_time_zone_type

        @selected_time_zone_type.setter
        def selected_time_zone_type(self, value):
            if value not in self._valid_time_zone_types:
                raise ValueError("")

            self._selected_time_zone_type = value

        @property
        def selected_time_zone(self):
            return _TimeZoneEnumManager().get_singleton().convert_value(
                self._selected_time_zone_type,
                _EnumConversionValue().CUSTOM,
            )

        def construct(self):
            global _ExternalDependencyManager

            global _TimeDataManager
            global _EnumConversionValue
            global _TimeZoneEnumManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _EnumConversionValue = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.enum_conversion_value",
                    member="EnumConversionValue",
                    is_member_callable=True,
                )
            )
            _TimeZoneEnumManager = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.time_zone_enum_manager",
                    member="TimeZoneEnumManager",
                    is_member_callable=True,
                )
            )
            _TimeDataManager = (
                _ExternalDependencyManager().get_singleton().import_module(
                    path="qlogicae_cor.v3.library.time_data_manager",
                    member="TimeDataManager",
                    is_member_callable=True,
                )
            )

            self.setup_properties({})

            return True

        def setup(self, **kwargs):
            if not kwargs:
                return True

            self.setup_properties(
                kwargs
            )

            return True            

        def shutdown(self):
            return True

        def setup_properties(self, kwargs):
            time_data_manager = (
                _TimeDataManager()
                    .get_singleton()
            )

            kwargs = (
                time_data_manager.write_setup_kwargs(
                    kwargs
                )
            )

            self._selected_time_zone_type = (
                kwargs.get(
                    "selected_time_zone_type",
                )
            )
            self._valid_time_zone_types = (
                kwargs.get(
                    "valid_time_zone_types",
                )
            )

            return True


    _TimeZoneManager = __TimeZoneManager
    _allocate = lambda: None


def TimeZoneManager():
    if _TimeZoneManager is None:
        _allocate()

    return _TimeZoneManager


# TimeZoneManager()
