__all__ = (
    "TimerManager",
)

_TimeManager = None
_ExternalDependencyManager = None

_TimeUnit = None
_TimerManager = None


def _allocate():
    global _allocate
    global _TimerManager

    from .abstract_manager import AbstractManager

    class __TimerManager(AbstractManager()):
        __slots__ = (
            "_start_timestamp",
            "_stop_timestamp",
        )

        def __init__(self):
            self.construct()

        @property
        def start_timestamp(self):
            return self._start_timestamp

        @property
        def stop_timestamp(self):
            return self._stop_timestamp

        def construct(self):
            global _ExternalDependencyManager

            if not _ExternalDependencyManager:
                from .external_dependency_manager import ExternalDependencyManager

                global _TimeUnit
                global _TimeManager

                _ExternalDependencyManager = (
                    ExternalDependencyManager()
                )

                _TimeManager = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.time_manager",
                        member="TimeManager",
                        is_member_callable=True,
                    )
                )
                _TimeUnit = (
                    _ExternalDependencyManager().read_singleton().import_module(
                        path="qlogicae_cor.v3.library.time_unit",
                        member="TimeUnit",
                        is_member_callable=True,
                    )
                )

            self._start_timestamp = 0
            self._stop_timestamp = 0

            return True

        def start_time(self):
            self._start_timestamp = (
                _TimeManager().read_singleton().current_nanosecond
            )

            return True

        def stop_time(self):
            self._stop_timestamp = (
                _TimeManager().read_singleton().current_nanosecond
            )

            return True

        def clear_time(self):
            self._start_timestamp = 0
            self._stop_timestamp = 0

            return True

        def reset_time(self):
            self._start_timestamp = (
                _TimeManager().read_singleton().current_nanosecond
            )
            self._stop_timestamp = 0

            return True

        def calculate_elapsed_time(self, time_unit=None):
            if time_unit is None:
                time_unit = _TimeUnit().SECOND

            TimeManager = (
                _TimeManager().read_singleton()
            )

            value = (
                TimeManager.convert_time_unit(
                    TimeManager.current_nanosecond - self._start_timestamp,
                    output_time_unit=time_unit,
                )
            )

            return value

        def calculate_duration_time(self, time_unit=None):
            if time_unit is None:
                time_unit = _TimeUnit().SECOND

            value = _TimeManager().read_singleton().convert_time_unit(
                self._stop_timestamp - self._start_timestamp,
                output_time_unit=time_unit,
            )

            return value

    _TimerManager = __TimerManager
    _allocate = lambda: None


def TimerManager():
    if _TimerManager is None:
        _allocate()

    return _TimerManager


# TimerManager()
