__all__ = (
    "TimestampManager",
)

_TimestampManager = None
_ExternalDependencyManager = None

_time = None
_datetime = None
_TimeUnit = None
_Timestamp = None
_TimeZoneDataManager = None
_TimestampDataManager = None

def _allocate():
    global _allocate
    global _TimestampManager

    class __TimestampManager:
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

            global _time
            global _datetime
            global _TimeUnit
            global _Timestamp
            global _TimeZoneDataManager
            global _TimestampDataManager

            from .external_dependency_manager import ExternalDependencyManager

            _ExternalDependencyManager = (
                ExternalDependencyManager()
            )

            _time = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="time"
                )
            )
            _datetime = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="datetime",
                )
            )
            _TimeUnit = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.time_unit",
                    member="TimeUnit",
                    is_member_callable=True,
                )
            )
            _TimeZoneDataManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.time_zone_data_manager",
                    member="TimeZoneDataManager",
                    is_member_callable=True,
                )
            )
            _TimestampDataManager = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.timestamp_data_manager",
                    member="TimestampDataManager",
                    is_member_callable=True,
                )
            )
            _Timestamp = (
                _ExternalDependencyManager().read_singleton().import_module(
                    path="qlogicae_cor.v3.library.timestamp",
                    member="Timestamp",
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

        def generate_current_timestamp(
            self,
            timestamp=None,
            time_unit=None,
        ):
            Timestamp = (
                _Timestamp()
            )
            TimeUnit = (
                _TimeUnit()
            )

            if timestamp is None:
                timestamp = Timestamp.ISO_DATE_STRING

            if time_unit is None:
                time_unit = TimeUnit.NANOSECOND

            timestamp_nanoseconds = _time().time_ns()

            current = _datetime().datetime.fromtimestamp(
                timestamp_nanoseconds / 1_000_000_000,
                _TimeZoneDataManager()
                    .read_singleton()
                    .read_selected_time_zone_type(),
            )

            timestamp_data_manager = (
                _TimestampDataManager()
                    .read_singleton()
            )

            match time_unit:
                case (
                    TimeUnit.NONE
                    | TimeUnit.SECOND
                ):
                    fraction = ""

                case TimeUnit.MILLISECOND:
                    fraction = (
                        f".{timestamp_nanoseconds // 1_000_000 % 1_000:03d}"
                    )

                case TimeUnit.MICROSECOND:
                    fraction = (
                        f".{timestamp_nanoseconds // 1_000 % 1_000_000:06d}"
                    )

                case TimeUnit.NANOSECOND:
                    fraction = (
                        f".{timestamp_nanoseconds % 1_000_000_000:09d}"
                    )

                case _:
                    fraction = ""

            if current.tzinfo is _datetime().UTC:
                suffix = "Z"
            else:
                suffix = current.strftime("%z")

                if suffix:
                    suffix = f"{suffix[:-2]}:{suffix[-2:]}"

            match timestamp:
                case Timestamp.ISO_DATE_STRING:
                    prefix = current.strftime(
                        timestamp_data_manager
                            .read_date_timestamp_format()
                    )

                case Timestamp.ISO_FILESYSTEM_STRING:
                    prefix = current.strftime(
                        timestamp_data_manager
                            .read_filesystem_timestamp_format()
                    )
                    suffix = suffix.replace(":", "-")

                case _:
                    return ""

            return "".join(
                (
                    prefix,
                    fraction,
                    suffix,
                )
            )

    _TimestampManager = __TimestampManager
    _allocate = lambda: None


def TimestampManager():
    if _TimestampManager is None:
        _allocate()

    return _TimestampManager


# TimestampManager()
